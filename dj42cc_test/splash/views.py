from django.shortcuts import redirect, render
from django.http import HttpResponseNotAllowed, HttpResponse
from forms import PersonContactsForm, PersonForm
from models import Person
from django.contrib.auth.decorators import login_required

@login_required
def edit_index_data(request):
    
    person = Person.objects.all().get()

    if request.method == 'GET':
        out_data = person.contacts
        for field in PersonForm.base_fields.keys():
            out_data[field] = getattr(person, field)

        form = PersonContactsForm(out_data)


    elif request.method == 'POST':
        form = PersonContactsForm(request.POST, instance=person)
    
        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        return HttpResponseNotAllowed("Method no allowed")

    
    kw = { "form" : form }

    return render(request, 'edit_person.html',kw)

