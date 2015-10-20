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
)
