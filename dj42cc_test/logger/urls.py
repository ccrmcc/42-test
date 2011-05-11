from django.views.generic.list_detail import object_list
from django.conf.urls.defaults import patterns, url

from models import HttpLogEntry

urlpatterns = patterns(
        '',
        url('^requests$', object_list,
            {"template_name": "show_requests.html",
                "queryset": HttpLogEntry.objects.all()[:10]}))
