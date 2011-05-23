from django.forms.models import modelformset_factory

from models import HttpLogEntry

HttpLogEntryFormSet = modelformset_factory(HttpLogEntry,
        fields=('priority',),
        extra=0,
)
