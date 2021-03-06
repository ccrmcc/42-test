from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj42cc_test.views.home', name='home'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),

    url(r'^', include('dj42cc_test.splash.urls')),
    url(r'^', include('dj42cc_test.logger.urls')),
    url(r'^settings', include('dj42cc_test.core.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
