from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('website.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^product/', include('product.urls')),
]
