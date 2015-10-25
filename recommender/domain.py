import pandas as pd

from recommender.utils import sim_pearson


class Recommender(object):

    def __init__(self, queryset):

        self.queryset = queryset
        self.dataset = pd.DataFrame(list(queryset))

    def top_matches(self, preferences, entity,n=5, similarity=sim_pearson):
        """
        Returns the best matches for entity from the preferences 
        dictionary. 
        Number of results and similarity function are optional 
        params.
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
