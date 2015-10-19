from django.conf.urls import include, url, patterns
from account import views

urlpatterns = patterns('',
    url(regex=r'^$',
        view = views.AccountListView.as_view(),
        name = 'account_list',
    ),
    url(regex=r'^add/$',
        view = 'account.views.customer_form',
        name = 'user_form',
    ),

)
