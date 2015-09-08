from django.core.management.base import BaseCommand

import pandas as pd

from recommender.utils import sim_pearson

import pickle

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        self.dataset = self._load_csv()

        user_prefs = self._fill_products()

        product_prefs = self.transform_prefs(user_prefs)

        itemsim = self.calculate_similar_items(user_prefs)

        with open('itemsim.pkl', 'wb') as arquivo:
            pickle.dump(itemsim, arquivo)
        """

        self.dataset = self._load_csv()

        user_prefs = self._fill_products()

    def _load_csv(self):
        return pd.read_csv('tmp/lances-sem-deposito.csv', sep=';',
                           names=['User', 'Product'])

    def _initialize_user_dict(self):
        di = {}
        for user in set(self.dataset.User):
            di[user] = {}
        return di

    def _fill_products(self):

        user_dict = self._initialize_user_dict()

        all_products = set(self.dataset.Product)

        for user in user_dict.keys():
            user_products = set(self.dataset[self.dataset.User == user].Product)

            for product in all_products:
                user_dict[user][product] = 0.0

            for product in user_products:
                user_dict[user][product] = 1.0

        return user_dict

    def top_matches(self, prefs,person,n=5,similarity=sim_pearson):
        """
        Returns the best matches for person from the prefs dictionary. 
        Number of results and similarity function are optional params.
        """

        scores=[(similarity(prefs,person,other),other) 
            for other in prefs if other!=person]
        scores.sort()
        scores.reverse()
        return scores[0:n]

    def get_recommendations(self, prefs,person,similarity=sim_pearson):
        """
        Gets recommendations for a person by using a weighted average
        of every other user's rankings
        """
        totals={}
        simSums={}

        for other in prefs:
            # don't compare me to myself
            if other==person: continue
            sim=similarity(prefs,person,other)

            # ignore scores of zero or lower
            if sim<=0: continue
            for item in prefs[other]:

                # only score movies I haven't seen yet
                if item not in prefs[person] or prefs[person][item]==0:
                    # Similarity * Score
                    totals.setdefault(item,0)
                    totals[item]+=prefs[other][item]*sim
                    # Sum of similarities
                    simSums.setdefault(item,0)
                    simSums[item]+=sim

        # Create the normalized list
        rankings=[(total/simSums[item],item) for item,total in totals.items()]

        # Return the sorted list
        rankings.sort()
        rankings.reverse()
        return rankings

    def transform_prefs(self, prefs):
        result={}
        for person in prefs:
            for item in prefs[person]:
                result.setdefault(item,{})

                # Flip item and person
                result[item][person]=prefs[person][item]

        return result


    def calculate_similar_items(self, prefs,n=10):
        """
        create a pre calculated structure to make faster the nexts
        searches

        Create a dictionary of items showing which other items they
        are most similar to.
        """
        result={}

        # Invert the preference matrix to be item-centric
        itemPrefs=self.transform_prefs(prefs)
        c=0
        for item in itemPrefs:

            # Satus updates for large datasets
            c+=1
            if c%100==0: print "%d / %d" % (c,len(itemPrefs))

            # Find the most similar items to this one
            scores=self.top_matches(itemPrefs,item,n=n,similarity=sim_pearson)
            result[item]=scores

        return result

    def get_recommended_products(self, prefs, item_match, user):
        """
        used to fast recommendations item_match is the return of 
        calculate_similar_items method.
        """

        userRatings=prefs[user]
        scores={}
        totalSim={}

        # Loop over items rated by this user
        for (item,rating) in userRatings.items():

            # Loop over items similar to this one
            for (similarity,item2) in item_match[item]:

                # Ignore if this user has already rated this item
                if item2 in userRatings: continue

                # Weighted sum of rating times similarity
                scores.setdefault(item2,0)
                scores[item2]+=similarity*rating

                # Sum of all the similarities
                totalSim.setdefault(item2,0)
                totalSim[item2]+=similarity

        # Divide each total score by total weighting to get an average
        rankings=[(score/totalSim[item],item) for item,score in scores.items()]

        # Return the rankings from highest to lowest
        rankings.sort()
        rankings.reverse()
        return rankings
