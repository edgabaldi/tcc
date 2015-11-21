#coding:utf-8
from core.views import SearchableListView, LoginRequiredMixin, MenuActiveMixin
from recommender.models import UserSimilarity
from recommender.forms import UserSimilaritySearchForm


class UserRecommendationView(MenuActiveMixin, LoginRequiredMixin,
                             SearchableListView):

    template_name = 'recommender/user_recommendation.html'
    model = UserSimilarity
    paginate_by=25
    form_class = UserSimilaritySearchForm
    menu_active = 'dashboard'
    submenu_active = 'user_recommendation'
