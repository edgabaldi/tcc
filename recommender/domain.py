import pandas as pd

from recommender.utils import sim_pearson
from recommender.models import ProductSimilarity
from product.models import Product, Bid


class Recommender(object):
    """
    Find the similarities based on preferences.

    Usage:
        The recommender class wait a list of dictonaries with pattern:

    Data Example:
        [{'user__id': 123, 'product__reference': 'brand+model+general-state'}]
    """

    def __init__(self, queryset):

        self.dataset = pd.DataFrame(list(queryset))

    def top_matches(self, preferences, entity, n=8, similarity=sim_pearson):
        """
        Returns the best matches for entity from the preferences dictionary.
        """

        scores=[(similarity(preferences, entity, other), other) 
            for other in preferences if other!=entity]
        scores.sort()
        scores.reverse()
        return scores[0:n]

    def get_recommendations(self, preferences, entity, similarity=sim_pearson):
        """
        Gets recommendations for a entity(user or item) by using 
        a weighted average of every other user's rankings
        """
        totals={}
        simSums={}

        for other in preferences:
            # don't compare me to myself
            if other==entity: continue
            sim=similarity(preferences,entity,other)

            # ignore scores of zero or lower
            if sim<=0: continue
            for item in preferences[other]:

                # only score movies I haven't seen yet
                if item not in preferences[entity] or preferences[entity][item]==0:
                    # Similarity * Score
                    totals.setdefault(item,0)
                    totals[item]+=preferences[other][item]*sim
                    # Sum of similarities
                    simSums.setdefault(item,0)
                    simSums[item]+=sim

        # Create the normalized list
        rankings=[(total/simSums[item],item) for item,total in totals.items()]

        # Return the sorted list
        rankings.sort()
        rankings.reverse()

        return rankings

    def initialize_user_dict(self):
        di = {}
        for user in self.dataset[self._unique_users_mask()].user__id:
            di[user] = {}
        return di

    def fill_products(self):

        user_dict = self.initialize_user_dict()

        for user in user_dict.keys():

            for product in self._all_products():
                user_dict[user][product] = 0.0

            for product in self._products_of_user(user):
                user_dict[user][product] = 1.0

        return user_dict

    def transform_preferences(self, preferences):
        result={}
        for entity in preferences:
            for item in preferences[entity]:
                result.setdefault(item,{})

                # Flip item and entity
                result[item][entity]=preferences[entity][item]

        return result

    def _unique_users_mask(self):
        return (self.dataset.user__id.duplicated()==False)

    def _unique_products_mask(self):
        return (self.dataset.product__reference.duplicated()==False)

    def _products_of_user(self, user):
        return set(self.dataset[self.dataset.user__id == user].product__reference)

    def _all_products(self):
        return self.dataset[self._unique_products_mask()].product__reference


class RecommendationCommand(object):

    @staticmethod
    def run():

        queryset = Bid.objects.values('user__id', 'product__reference')

        cmd = Recommender(queryset)
        user_prefs = cmd.fill_products()
        item_prefs = cmd.transform_preferences(user_prefs)

        product_list = Product.objects.filter(status='liberado_lance')

        for product in product_list:

            recommendation = cmd.top_matches(item_prefs, product.reference)

            for score, other_reference in recommendation:

                other_list = product_list.filter(reference=other_reference)

                if len(other_list) > 0:

                    other_product = other_list[0]

                    assert product != other_product

                    similar = ProductSimilarity(
                        score=score,
                        product=product,
                        is_similar_to=other_product)

                    similar.save()
