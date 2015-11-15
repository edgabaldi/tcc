#coding:utf-8
from core.views import SearchableListView, LoginRequiredMixin 
from recommender.models import UserSimilarity
from recommender.forms import UserSimilaritySearchForm


class UserRecommendationView(LoginRequiredMixin, SearchableListView):

    template_name = 'recommender/user_recommendation.html'
    model = UserSimilarity
    paginate_by=25
    form_class = UserSimilaritySearchForm
