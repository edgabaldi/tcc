#coding:utf-8
import pandas as pd
import numpy as np

from recommender.models import ProductSimilarity
from recommender.cache import SQLiteCacheBackend
from product.models import Product, Bid

# constants
ITEM_BASED, USER_BASED = 'ITEM_BASED', 'USER_BASED'


class Model(object):

    def __init__(self, queryset):

        self.cache = SQLiteCacheBackend()
        self.data = pd.DataFrame(list(queryset))

    def create(self):

        prefs = self._fill_products()
        self.cache['prefs'] = prefs

    def get_preferences(self):
        return self.cache['prefs']

    def _initialize_user_dict(self):

        di = {}
        for user in self.data[self._unique_users_mask()].user__id:
            di[user] = {}
        return di

    def _fill_products(self):

        user_dict = self._initialize_user_dict()

        for user in user_dict.keys():

            for product in self._all_products():
                user_dict[user][product] = 0

            for product in self._products_of_user(user):
                user_dict[user][product] = 1

        return pd.DataFrame(user_dict)

    def _unique_users_mask(self):
        return (self.data.user__id.duplicated()==False)

    def _unique_products_mask(self):
        return (self.data.product__reference.duplicated()==False)

    def _products_of_user(self, user):
        return set(self.data[self.data.user__id == user].product__reference)

    def _all_products(self):
        return self.data[self._unique_products_mask()].product__reference


class Recommender(object):
    """
    Find the similarities based on preferences.
    """

    def __init__(self, preferences):

        self.preferences = preferences

    def similar_items(self, item_id, n=None, only_positive_corr=True):
        """
        Returns a ranked list of similar items.
        Based on: https://goo.gl/3gwAlTyy
        """
        # similar_ix: ix1, transpose=False, n=None, only_positive_corr=False
        return self.similar_ix(**{
            'ix1': item_id,
            'n': n,
            'only_positive_corr': only_positive_corr,
            'transpose': False})

    def recommend_items(self, user_id, n=None, only_positive_corr=True, method=USER_BASED):
        """
        Returns a ranked list of recommended items for a user, using a row or column based approach.
        """
        # recommend_cols: ix, transpose=False, only_positive_corr=True, n=None, binary=False
        kwargs = {
            'ix': user_id,
            'transpose': True,
            'n': n,
            'binary': True,
            'only_positive_corr': only_positive_corr
        }
        if method == USER_BASED:
            return self.recommend_cols(**kwargs)
        # else it's item based
        # recommend_cols_bycol: ix, transpose=False, n=None, binary=False
        # we need to pop only_positive_corr
        kwargs.pop('only_positive_corr')
        return self.recommend_cols_bycol(**kwargs)


    def recommend_cols(self, ix, transpose=False, only_positive_corr=True, n=None, binary=False):
        """
        Return row based recommended columns for specific index.
        Based on: https://goo.gl/3gwAlTyy
        """
        assert type(transpose) is bool
        assert type(binary) is bool

        #first get similar rows by score and unreviewed cols for ix
        # similar_ix: ix1, transpose, n, only_positive_corr
        sims = self.similar_ix(**{
            'ix1': ix, 
            'transpose': transpose, 
            'only_positive_corr': only_positive_corr, 
            'n': n})
         # if there are no similarities we cannot make recommendations
        if len(sims) == 0:
            return []
        # we have sims, let's move on
        # transpose df?
        df = self.preferences.transpose() if transpose else self.preferences
        # get similarities 
        sim_score, index = map(np.asarray, zip(*sims))
        not_reviewed = df.columns[df.ix[ix].fillna(0) == 0]
        # filter relevant info
        df_sub = df.loc[index, not_reviewed]
        if df_sub.empty:
            return []
        # calculate weighted ratings
        weighted_ratings = df_sub.apply(lambda x: x*sim_score).sum()
        # sum similarity scores in order to normalize weighted 
        # ratings -- we don't want a very popular column to bias recommendations
        # in the case of rating engines, we just need to add anyting that is > 0
        # but in the case of binary engines, rating 0 is the same as "reviewing 0",
        # which means that we have to take into account all similarity scores and 
        # not just the "active" ones
        sum_sim_score = sim_score.sum() if binary else (df_sub > 0).apply(lambda x: x*sim_score).sum()
        # recommended columns are now normalized by sum of sim scores
        recs = weighted_ratings/sum_sim_score
        # are there any np.nan values or zero values in recs?
        # we may still have these, as only_positive_corr only 
        # assures positively correlated rows, but has nothing 
        # to say about which col values can be considered "active"
        recs = recs[recs > 0]
        n = n if (type(n) is int and n > 0) else len(recs)
        return sorted(zip(recs.values, recs.index), reverse=True)[:n]


    def _similar_ix_inner(self, ix1, transpose=False):
        """
        This method returns every similar_ix to ix1. The idea is to avoid 
        recalculating similar_ix for different values of n and only_positive_corr.

        This is the *core method of the engine*, so it needs to be very efficient.
        Based on: https://goo.gl/3gwAlTyy
        """
        #transpose dataframe?
        df = self.preferences.transpose() if transpose else self.preferences
        _pcorr = lambda i, j: df.ix[[i, j]].transpose().corr().fillna(0, inplace=False).loc[i, j]
        def _inner(i,j):
            try:
                return _pcorr(i, j)
            except:
                raise Exception(", ".join([str(i), str(j)]))
        # this returns an unsorted list of similarities. there is *no value checking at all*,
        # so use wrapping methods, such as similar_ix or recommend_cols to acces these values
        return [(_inner(ix1, ix2), ix2) for ix2 in df.index if ix1 != ix2]

    def similar_ix(self, ix1, transpose=False, n=None, only_positive_corr=False):
        """
        Return a sorted list of pearson-similar indexes, for a given index and dataframe.
        Based on: https://goo.gl/3gwAlTyy
        """
        assert type(only_positive_corr) is bool
        similar = self._similar_ix_inner(ix1=ix1, transpose=transpose)
        if only_positive_corr:
            similar = [(score, ix) for (score, ix) in similar if score > 0]
            n = n if (type(n) is int and n > 0) else len(similar)
        return sorted(similar, reverse=True)[:n]


class RecommendationCommand(object):

    @staticmethod
    def run():

        # train model
        queryset = Bid.objects.values('user__id', 'product__reference').distinct()
        model = Model(queryset)
        model.create()

        # prepare recommendation
        recommender = Recommender(model.get_preferences())

        product_list = Product.objects.filter(status='liberado_lance').distinct()

        for product in product_list:

            print product.reference

            # find similar products
            similars = recommender.similar_items(product.reference, n=8)

            # save similar products
            instance_list = []
            for score, other_reference in similars:

                if product.reference != other_reference:

                    other_products = product_list.filter(
                        similars=None,
                        reference=other_reference)

                    if len(other_products) > 0:

                        other_product = other_products[0]

                        print product.reference + ' -> ' + other_reference

                        instance_list.append(ProductSimilarity(
                            score=score,
                            product=product,
                            is_similar_to=other_product))

            ProductSimilarity.objects.bulk_create(instance_list)
