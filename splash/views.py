from django.shortcuts import render_to_response
from models import Person

def show_person(request):
    person = Person.objects.get()
    tpl_kw = {
            "person" : person
    }
    return render_to_response('show_person.html', tpl_kw)
