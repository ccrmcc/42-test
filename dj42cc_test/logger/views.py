from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from models import HttpLogEntry
from forms import HttpLogEntryFormSet


def show_requests(request):

    object_list = HttpLogEntry.objects.order_by("-priority")
    formset = HttpLogEntryFormSet(queryset=object_list)

    kw = {
            "object_list": object_list,
            "formset": formset,
            "object_form": zip(object_list, formset),
    }

    return render(request, "show_requests.html", kw)


@login_required
def edit_requests(request):
    formset = HttpLogEntryFormSet(request.POST)

    if formset.is_valid():
        formset.save()

    return redirect("show_requests")
