#coding:utf-8
import pandas as pd

from recommender.models import ProductSimilarity
from recommender.cache import SQLiteCacheBackend
from product.models import Product, Bid


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

    def find_similars_to(self, entity, n=8, transpose=False):

        df = self.preferences.transpose() if transpose else self.preferences

        _pcorr = lambda i, j: df.ix[[i, j]].transpose().corr().fillna(0, inplace=False).loc[i, j]

        def _inner(i,j):
            try:
                return _pcorr(i, j)
            except:
                raise Exception(u", ".join([str(i), str(j)]))

        matches = [(_inner(entity, other), other) for other in df.index if entity != other]

        similar = [(score, other) for (score, other) in matches if score > 0]

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
            similars = recommender.find_similars_to(product.reference)

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
