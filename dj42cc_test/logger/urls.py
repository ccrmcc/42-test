from django.conf.urls.defaults import patterns, url

from models import HttpLogEntry

urlpatterns = patterns(
        'dj42cc_test.logger.views',
        url('^requests$', "show_requests", name="show_requests"),
        url('^requests/edit$', "edit_requests", name="edit_requests"),
)
