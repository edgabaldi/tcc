from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
    url(regex=r'^$',
        view = 'website.views.index',
        name = 'index'
    ),
    url(regex=r'^show_product/$',
        view = 'website.views.product',
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


