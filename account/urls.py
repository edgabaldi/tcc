from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
    url(regex=r'^$',
        view = 'account.views.customer_list',
        name = 'customer_list',
    ),
    url(regex=r'^add/$',
        view = 'account.views.customer_form',
        name = 'customer_form',
    ),

)
