from django.forms import ModelForm
from django.forms import widgets
from django.forms.models import inlineformset_factory

from django import forms
from models import Person, Contact, OtherContact

from .widgets import JqueryDate


class PersonForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
                "birth_date": JqueryDate,
        }
        fields = ('last_name', 'first_name', 'bio', 'birth_date',)


class OtherContactForm(ModelForm):
    class Meta:
        model = OtherContact

ContactFormSet = inlineformset_factory(Person, Contact, extra=0)
