from django.shortcuts import render, redirect
from django.contrib import messages

from fair.models import Fair
from participant.models import Participant
from catalog.models import Catalog
from catalog_item.models import CatalogItem
from .models import Entry

from .forms import EntryForm


def index(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Request was saved successfully")
            return redirect("entry_home")

        messages.error(request, form.errors)

    # Participants - Dropdown
    active_fair = Fair.objects.get(owner=request.user, active=True)
    participants = Participant.objects.filter(fair=active_fair)

    # Catalog Items - Dropdown
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    catalog_items = CatalogItem.objects.filter(catalog=catalog)

    # Table List
    # entries = Entry.entry_catalog_item.filter(catalog=catalog)
    entries = Entry.objects.filter(catalog_item__catalog=catalog)
    print(entries)

    context = {
        'participants': participants,
        'catalog_items': catalog_items,
        "entries": entries
    }
    return render(request, "entries.html", context)


def delete(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    entry.delete()
    messages.success(request, "Entry was deleted  successfully")
    return redirect('entry_home')