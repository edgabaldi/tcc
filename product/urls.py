from django.conf.urls import include, url, patterns
from product import views

urlpatterns = patterns('',
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

)
