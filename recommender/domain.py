import pandas as pd

from recommender.utils import sim_pearson
from recommender.models import ProductSimilarity
from recommender.cache import SQLiteCacheBackend
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

        self.cache = SQLiteCacheBackend()
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
        cmd.cache['user_prefs'] = cmd.fill_products()
        cmd.cache['item_prefs'] = cmd.transform_preferences(cmd.cache['user_prefs'])

        product_list = Product.objects.filter(status='liberado_lance')

        for product in product_list:

            print product.reference

            recommendation = cmd.top_matches(cmd.cache['item_prefs'], product.reference)

            for score, other_reference in recommendation:
                print product.reference + ' -> ' + other_reference

                other_list = product_list.filter(reference=other_reference)

                if len(other_list) > 0:

                    other_product = other_list[0]

                    assert product != other_product

                    similar = ProductSimilarity(
                        score=score,
                        product=product,
                        is_similar_to=other_product)

                    similar.save()
