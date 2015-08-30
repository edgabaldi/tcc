from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
    url(regex=r'^$',
        view = 'product.views.product_list',
        name = 'product_list',
    ),
    url(regex = r'^add/$',
        view = 'product.views.product_form',
        name = 'product_form',
    ),
)
