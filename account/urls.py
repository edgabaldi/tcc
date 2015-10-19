from django.conf.urls import include, url, patterns
from account import views

urlpatterns = patterns('',
    url(regex=r'^$',
        view = views.UserListView.as_view(),
        name = 'user_list',
    ),
    url(regex=r'^add/$',
        view = views.UserCreateView.as_view(),
        name = 'user_add',
    ),

)
