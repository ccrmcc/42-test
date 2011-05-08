from django.forms import ModelForm
from django.forms import widgets
from django import forms
from models import Person

class PersonForm(ModelForm):
    class Meta:
        model = Person

class PersonContactsForm(PersonForm):
    email = forms.EmailField()
    skype = forms.CharField()
    jabber = forms.EmailField()
    other = forms.CharField(widget=widgets.Textarea)
