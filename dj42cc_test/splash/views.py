from django.shortcuts import redirect, render
from forms import PersonForm, ContactFormSet, OtherContactForm
from models import Person
from django.contrib.auth.decorators import login_required


@login_required
def edit_index_data(request):

    person = Person.objects.all().get()
    other = person.othercontact_set.all().get()

    if request.method == 'GET':
        form = PersonForm(instance=person)
        contact_formset = ContactFormSet(instance=person)
        othercontact_form = OtherContactForm(instance=other)

        kw = {
                "form": form,
                "contact" : contact_formset,
                "other" : othercontact_form,
        }

        return render(request, 'edit_person.html', kw)

    form = PersonForm(request.POST, instance=person)
    contact_formset = ContactFormSet(request.POST, instance=person)
    othercontact_form = OtherContactForm(request.POST, instance=other)

    if form.is_valid() and contact_formset.is_valid() and \
            othercontact_form.is_valid():
        form.save()
        contact_formset.save()
        othercontact_form.save()


        return redirect('/')

    assert False, "non implemented yet"
