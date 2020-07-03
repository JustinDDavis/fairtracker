from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

from fair.models import Fair
from participant.models import Participant
from catalog.models import Catalog
from catalog_item.models import CatalogItem
from prize.models import Prize
from entry.models import Entry
from .models import JudgeSheet

from .forms import JudgeSheetForm


def index(request):
    if request.method == "POST":
        form = JudgeSheetForm(request.POST)
        if form.is_valid():
            # Make sure the Participant actually enrolled in the Catalog Item.
            participant = form.cleaned_data['participant']
            catalog_item = form.cleaned_data['catalog_item']
            try:
                results = Entry.objects.get(participant=participant, catalog_item=catalog_item)
            except ObjectDoesNotExist as err:
                messages.error(request, f"Participant ({participant.name}) did not enter in catalog item ({catalog_item.name})")
                return redirect("judge_sheet_home")
            form.save()
            messages.success(request, "Request was saved successfully")
            return redirect("judge_sheet_home")

        messages.error(request, form.errors)
        return redirect("judge_sheet_home")

    # Participants - Dropdown
    active_fair = Fair.objects.get(owner=request.user, active=True)
    participants = Participant.objects.filter(fair=active_fair)

    # Catalog Items - Dropdown
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    prizes = Prize.objects.filter(catalog=catalog)

    # Entries - Dropdown
    catalog_items = CatalogItem.objects.filter(catalog=catalog)
    print(catalog_items)

    # Table List
    judge_sheets = JudgeSheet.objects.filter(participant__fair=active_fair)
    print(judge_sheets)

    context = {
        'participants': participants,
        'prizes': prizes,
        'catalog_items': catalog_items,
        "judge_sheets": judge_sheets
    }

    return render(request, "judge_sheet.html", context)


def delete(request, judge_sheet_id):
    judge_sheet = JudgeSheet.objects.get(pk=judge_sheet_id)
    judge_sheet.delete()
    messages.success(request, "Judge Sheet was deleted  successfully")
    return redirect('judge_sheet_home')