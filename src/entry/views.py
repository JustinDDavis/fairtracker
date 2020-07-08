from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.functions import Lower

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

    sort_column = request.GET.get('sort', '')
    if sort_column in ["participant", "-participant"]:
        # sort=author
        if sort_column[0] == "-":
            entries = entries.order_by(Lower("participant__name").desc())
        else:
            entries = entries.order_by(Lower("participant__name"))

    elif sort_column in ["catalog_item", "-catalog_item"]:
        if sort_column[0] == "-":
            entries = entries.order_by(Lower("catalog_name__name").desc())
        else:
            entries = entries.order_by(Lower("catalog_name__name"))
    else:
        entries = entries.order_by(Lower("participant__name"))

    context = {
        'participants': participants,
        'catalog_items': catalog_items,
        "entries": entries
    }
    return render(request, "entries.html", context)


def edit(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)

    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry Updated Successfully")
            return redirect("entry_home")
        messages.error(request, form.errors)
        return redirect("entry_edit")
    else:
        # Participants - Dropdown
        active_fair = Fair.objects.get(owner=request.user, active=True)
        participants = Participant.objects.filter(fair=active_fair)

        # Catalog Items - Dropdown
        catalog = Catalog.objects.get(fair=active_fair, active=True)
        catalog_items = CatalogItem.objects.filter(catalog=catalog)

        context = {
            "entry": entry,
            "participants": participants,
            "catalog_items": catalog_items
        }
        return render(request, "edit_entry.html", context)

def delete(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    entry.delete()
    messages.success(request, "Entry was deleted  successfully")
    return redirect('entry_home')