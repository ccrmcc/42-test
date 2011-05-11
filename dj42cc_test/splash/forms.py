from django.forms import ModelForm
from django.forms import widgets
from django import forms
from models import Person

from .widgets import JqueryDate


class PersonForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
                "birth_date": JqueryDate,
        }


class PersonContactsForm(PersonForm):
    CONTACT_TYPES = ['email', 'skype', 'jabber', 'other']
    email = forms.EmailField()
    skype = forms.CharField()
    jabber = forms.EmailField()
    other = forms.CharField(widget=widgets.Textarea)

    def contact_fields(self):
        return [
                (typ, self[typ])
                for typ in
                self.CONTACT_TYPES]

    def save(self):

        self.instance.contacts = self.cleaned_data

        super(PersonContactsForm, self).save()
