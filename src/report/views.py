from django.shortcuts import render

from fair.models import Fair
from participant.models import Participant
from catalog.models import Catalog
from judge_sheet.models import JudgeSheet
from entry.models import Entry


def index(request):
    # Particpants
    active_fair = Fair.objects.get(owner=request.user, active=True)
    participants = Participant.objects.filter(fair=active_fair)

    # Entries
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    entries = Entry.objects.filter(catalog_item__catalog=catalog)

    # Prizes
    judge_sheets = JudgeSheet.objects.filter(catalog_item__catalog=catalog)

    context = {
        "participants": participants,
        "entries": entries,
        "judge_sheets": judge_sheets
    }

    return render(request, "reports.html", context)

def printer(request):
    # Particpants
    active_fair = Fair.objects.get(owner=request.user, active=True)
    participants = Participant.objects.filter(fair=active_fair)

    # Entries
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    entries = Entry.objects.filter(catalog_item__catalog=catalog)

    # Prizes
    judge_sheets = JudgeSheet.objects.filter(catalog_item__catalog=catalog)

    context = {
        "participants": participants,
        "entries": entries,
        "judge_sheets": judge_sheets
    }

    return render(request, "report_printout.html", context)