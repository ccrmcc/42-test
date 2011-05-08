from django.shortcuts import redirect, render
from forms import PersonForm
from models import Person

def edit_index_data(request):
    
    person = Person.objects.all().get()

    if request.method == 'GET':
        form = PersonForm(instance=person)

        kw = { "form" : form }

        return render(request, 'edit_person.html',kw)



    form = PersonForm(request.POST, instance=person)
    
    if form.is_valid():
        form.save()

        return redirect('/')
    
    assert False, "non implemented yet"

