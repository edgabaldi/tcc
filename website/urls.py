from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
    url(regex=r'^$',
        view = 'website.views.index',
        name = 'index'
    ),
    url(regex=r'^product$',
        view = 'website.views.product',
        name = 'product',
    ),
    url(regex=r'^cadastrar$',
        view = 'website.views.signin',
        name = 'signin',
    ),
)


