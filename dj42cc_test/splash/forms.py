from django.forms import ModelForm
from django.forms import widgets
from django import forms
from models import Person

class PersonForm(ModelForm):
    class Meta:
        model = Person

class PersonContactsForm(PersonForm):
    CONTACT_TYPES = [ 'email', 'skype', 'jabber', 'other' ]
    email = forms.EmailField()
    skype = forms.CharField()
    jabber = forms.EmailField()
    other = forms.CharField(widget=widgets.Textarea)

    def contact_fields(self):
        return [
                (typ, self[typ])
                for typ in
                self.CONTACT_TYPES
        ]
