from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
    url(regex=r'^$',
        view = 'website.views.index',
        name = 'index'),
)


