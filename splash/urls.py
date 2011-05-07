from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
        'dj42cc_test.splash.views',
        url('^$', 'show_person'),
)
