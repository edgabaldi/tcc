from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
    url(regex=r'^$',
        view = 'customer.views.customer_list',
        name = 'customer_list',
    ),
    url(regex=r'^add/$',
        view = 'customer.views.customer_form',
        name = 'customer_form',
    ),

)
