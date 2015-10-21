from django.conf.urls import include, url, patterns
from product import views

urlpatterns = patterns('',

    #
    # Product Views
    #

    url(regex=r'^$',
        view = views.ProductSearchableListView.as_view(),
        name = 'product_list',
    ),
    url(regex = r'^add/$',
        view = views.ProductCreateView.as_view(),
        name = 'product_add',
    ),
    url(regex = r'^(?P<pk>\d+)/$',
        view = views.ProductUpdateView.as_view(),
        name = 'product_edit',
    ),
    url(regex = r'^(?P<pk>\d+)/delete/$',
        view = views.ProductDeleteView.as_view(),
        name = 'product_delete',
    ),

    #
    # Brand Views
    #
    url(regex=r'^brand/$',
        view = views.BrandSearchableListView.as_view(),
        name = 'brand_list',
    ),


)
