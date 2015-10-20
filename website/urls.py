from django.conf.urls import include, url, patterns
from website import views

urlpatterns = patterns('',
    url(regex=r'^$',
        view = views.ProductListView.as_view(),
        name = 'index'
    ),
    url(regex=r'^show/(?P<pk>\d+)/$',
        view = views.ProductDetailView.as_view(),
        name = 'product',
    ),
    url(regex=r'^cadastrar/$',
        view = views.SignUpCreateView.as_view(),
        name = 'signup',
    ),
    url(regex=r'^login/$',
        view = 'website.views.login',
        name = 'login',
    ),
    url(regex=r'^system/dashboard/$',
        view = 'website.views.dashboard',
        name = 'dashboard',
    ),
)


