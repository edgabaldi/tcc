from django.conf.urls import include, url, patterns
from django.contrib.auth import views as auth_views
from account.forms import CustomAuthenticationForm

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
        view = auth_views.login,
        name = 'login',
        kwargs = {'authentication_form': CustomAuthenticationForm},
    ),
    url(regex=r'^logout/$',
        view = auth_views.logout,
        name = 'logout',
        kwargs = {'next_page': '/'},
    ),
    url(regex=r'^system/dashboard/$',
        view = 'website.views.dashboard',
        name = 'dashboard',
    ),
)


