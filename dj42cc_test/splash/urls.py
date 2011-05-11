from django.views.generic.list_detail import object_detail
from django.conf.urls.defaults import patterns, url

from models import Person

urlpatterns = patterns(
        'dj42cc_test.splash.views',
        url('^$', object_detail,
            {"template_name": "show_person.html",
                "queryset": Person.objects,
                "object_id": 1,
                "template_object_name": "person",
            },
        ),
        url('^contact_edit$', 'edit_index_data'),
        url('^contact_edit/ajax$', 'edit_index_data_ajax'),
)
