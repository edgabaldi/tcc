from django.conf.urls import include, url, patterns
from recommender import views

urlpatterns = patterns('',

    url(regex=r'^user/$',
        view = views.UserRecommendationView.as_view(),
        name = 'user_recommendation',
    ),
)

