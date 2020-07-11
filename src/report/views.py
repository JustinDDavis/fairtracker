import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models.functions import Lower

from fair.models import Fair
from participant.models import Participant
from catalog.models import Catalog
from judge_sheet.models import JudgeSheet
from entry.models import Entry


def index(request):
    # Particpants
    active_fair = Fair.objects.get(owner=request.user, active=True)
    participants = Participant.objects.filter(fair=active_fair).order_by(Lower("name"))

    # Entries
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    entries = Entry.objects.filter(catalog_item__catalog=catalog)

    # Prizes
    judge_sheets = JudgeSheet.objects.filter(catalog_item__catalog=catalog)

    processed_values = process_for_display(participants, entries, judge_sheets)
    print(processed_values)

    context = {
        "processed_values": processed_values
    }

    return render(request, "reports.html", context)

def printer(request):
    # Particpants
    active_fair = Fair.objects.get(owner=request.user, active=True)
    participants = Participant.objects.filter(fair=active_fair).order_by(Lower("name"))

    # Entries
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    entries = Entry.objects.filter(catalog_item__catalog=catalog)

    # Prizes
    judge_sheets = JudgeSheet.objects.filter(catalog_item__catalog=catalog)

    processed_values = process_for_display(participants, entries, judge_sheets)

    context = {
        "processed_values": processed_values
    }

    return render(request, "report_printout.html", context)


def report_export_participants(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="FairTracker_Participant_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Fair Name', 'Participant Name', 'Participant Email', 'Participant City', 'Participant Manual ID'])

    # Particpants
    active_fair = Fair.objects.get(owner=request.user, active=True)
    participants = Participant.objects.filter(fair=active_fair).order_by(Lower("name"))

    for participant in participants:
        writer.writerow([active_fair.name, participant.name, participant.email, participant.city, participant.static_participant_id])

    return response


def process_for_display(participants, entries, judge_sheets):
    # {
    #     data: [
    #         {
    #             "participant": {
    #                 "name"...
    #             },
    #             "entries": {
    #
    #             },
    #             "awards": {
    #
    #             },
    #             "calculated": {
    #                 "total_awarded"...
    #             }
    #         }
    #     ]
    # }
    return_object = []

    for participant in participants:
        new_data = {}
        # Add Participant Data
        new_data["participant"] = {
            "name": participant.name,
            "city": participant.city,
            "email": participant.email,
            "id": participant.id if not participant.static_participant_id else participant.static_participant_id
        }

        new_data["entries"] = []
        new_data["awards"] = []
        new_data["calculated"] = {}
        for entry in entries:
            # Add entries:
            if entry.participant.id == participant.id:
                new_data["entries"].append({
                    "name": entry.catalog_item.name,
                    "description": entry.catalog_item.description
                })

        for judge_sheet in judge_sheets:
            if judge_sheet.participant.id == participant.id:
                new_data["awards"].append({
                    "entry_name": judge_sheet.catalog_item.name,
                    "prize_name": judge_sheet.prize.name,
                    "prize_amount": judge_sheet.prize.amount
                })

        for calc_awards in new_data["awards"]:
            print(calc_awards)
            new_data["calculated"].update({
                "total_awarded": new_data["calculated"].get("total_awarded", 0) + calc_awards["prize_amount"]
            })

        return_object.append(new_data)

    print(return_object)
    return {
        "data": return_object
    }