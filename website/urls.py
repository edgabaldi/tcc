from django.conf.urls import include, url, patterns
from website import views

urlpatterns = patterns('',
    url(regex=r'^$',
        view = views.ProductListView.as_view(),
        name = 'index'
    ),
    url(regex=r'^product/(?P<pk>\d+)/$',
        view = views.ProductDetailView.as_view(),
        name = 'product',
    ),
    url(regex=r'^cadastrar/$',
        view = 'website.views.signin',
        name = 'signin',
    ),
    url(regex=r'^login/$',
        view = 'website.views.login',
        name = 'login',
    ),
    url(regex=r'^sistema/dashboard/$',
        view = 'website.views.dashboard',
        name = 'dashboard',
    ),
)


