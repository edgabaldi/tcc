from math import sqrt

def sim_pearson(preferences, p1, p2):
    """
    Get the list of mutually rated items
    """
    si={}
    for item in preferences[p1]: 
        if item in preferences[p2]: si[item]=1

    # if they are no ratings in common, return 0
    if len(si)==0: return 0

    # Sum calculations
    n=len(si)

    # Sums of all the preferences
    sum1=sum([preferences[p1][it] for it in si])
    sum2=sum([preferences[p2][it] for it in si])

    # Sums of the squares
    sum1Sq=sum([pow(preferences[p1][it],2) for it in si])
    sum2Sq=sum([pow(preferences[p2][it],2) for it in si])	

    # Sum of the products
    pSum=sum([preferences[p1][it]*preferences[p2][it] for it in si])

    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0

    r=num/den

    return r
