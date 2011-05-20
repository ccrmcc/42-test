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


class OtherContactForm(ModelForm):
    class Meta:
        model = OtherContact

ContactFormSet = inlineformset_factory(Person, Contact, extra=0)
