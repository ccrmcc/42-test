from django.shortcuts import redirect
from forms import PersonForm
from models import Person

def edit_index_data(request):
    
    person = Person.objects.all().get()

    form = PersonForm(request.POST, instance=person)
    
    if form.is_valid():
        form.save()

        return redirect('/')
    
    assert False, "non implemented yet"

