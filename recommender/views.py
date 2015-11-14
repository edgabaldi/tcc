from django.views.generic import TemplateView


class UserRecommendationView(TemplateView):
    template_name = 'recommender/user_recommendation.html'
