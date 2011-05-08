from django.shortcuts import redirect, render
from forms import PersonContactsForm, PersonForm
from models import Person

def edit_index_data(request):
    
    person = Person.objects.all().get()

    if request.method == 'GET':
        out_data = person.contacts
        for field in PersonForm.base_fields.keys():
            out_data[field] = getattr(person, field)

        form = PersonContactsForm(out_data)

        kw = { "form" : form }

        return render(request, 'edit_person.html',kw)



    form = PersonContactsForm(request.POST, instance=person)
    
    if form.is_valid():
        form.save()

        person.contacts = form.cleaned_data # save contacts

        return redirect('/')
    
    assert False, "non implemented yet"

