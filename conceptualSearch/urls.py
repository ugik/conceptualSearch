from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^user/', include('Auth.urls')),
    (r'^$', 'conceptualSearch.views.index'),
    (r'^search-form/$', 'conceptualSearch.views.search_form'),
    (r'^search/$', 'conceptualSearch.views.search'),
 )

