import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models.functions import Lower

from fair.models import Fair
from participant.models import Participant
from catalog.models import Catalog
from catalog_item.models import CatalogItem
from judge_sheet.models import JudgeSheet
from entry.models import Entry
from prize.models import Prize

import time

def index(request):
    start_time = time.time()
    # your code
    # Particpants
    active_fair = Fair.objects.get(owner=request.user, active=True)
    participants = Participant.objects.filter(fair=active_fair).order_by(Lower("name"))
    
    print(f"Report AF/Part: {str(time.time() - start_time)}")

    # Entries
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    entries = Entry.objects.filter(catalog_item__catalog=catalog)
    
    print(f"Report Catalog and entries: {str(time.time() - start_time)}")

    # Prizes
    judge_sheets = JudgeSheet.objects.filter(catalog_item__catalog=catalog)
    
    print(f"Report Judgesheets: {str(time.time() - start_time)}")

    processed_values = process_for_display(participants, entries, judge_sheets)
    
    print(f"Report done processing: {str(time.time() - start_time)}")

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

def report_export_entries(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="FairTracker_Entries_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Fair Name', 'Participant Name', 'Participant Manual ID', 'Entry ID', 'Entry Description'])

    # Particpants
    active_fair = Fair.objects.get(owner=request.user, active=True)
    participants = Participant.objects.filter(fair=active_fair).order_by(Lower("name"))

    # Entries
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    entries = Entry.objects.filter(catalog_item__catalog=catalog)

    data = process_for_display(participants, entries, [])

    for row in data["data"]:
        for entry in row["entries"]:
            writer.writerow([active_fair.name,
                             row["participant"]["name"],
                             row["participant"].get("static_participant_id", row["participant"].get("id", "-")),
                             entry["name"],
                             entry["description"]])

    return response

def report_full_fair(request):
    # List all entries
    active_fair = Fair.objects.get(owner=request.user, active=True)
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    catalog_items = CatalogItem.objects.filter(catalog=catalog).order_by("name")

    # Get all Prices
    prizes = Prize.objects.filter(catalog=catalog).order_by("-amount", "name")

    # I need a nxn Matrix. First column will be the Catalog Items
    # The columns will be the prizes.
    # I want the winner name in the column of their prize.
    #  Maybe a dictionary to store the prize and their matching index?
    # {
    #   "award 1": 1,
    #   "award blue: 2,
    # }

    matrix_map = {}
    column_offset = 1
    for index, prize in enumerate(prizes):
        matrix_map[prize.name] = index + column_offset

    # Get number of columns
    number_of_columns = len(matrix_map.keys()) + 1
    # Get number of rows
    number_of_rows = len(catalog_items) + 1

    print(f"number of columns: {number_of_columns}")
    print(f"number of rows: {number_of_rows}")

    report_array = [["" for x in range(number_of_columns + 1)] for y in range(number_of_rows + 1)]

    # Populate Header:
    report_array[0][0] = "Catalog Item Names"
    for prize_name in matrix_map.keys():
        # I need to place at the dictionary value in this first row
#         print(f"temp-test: {prize_name}")
#         print(f"temp-test-matrix: {matrix_map[prize_name]}")
#         print(f"temp-test-length: {report_array[0]}")
        report_array[0][matrix_map[prize_name]] = prize_name



    # To through the Catalog Items
    # Get all the Judge sheets of this catalog item.
    #
    for index, catalog_item in enumerate(catalog_items):
        report_array[index+1][0] = catalog_item.name

        judge_sheets = JudgeSheet.objects.filter(catalog_item=catalog_item)
        for judge_sheet in judge_sheets:
            prize_name = judge_sheet.prize.name
            report_array_location = matrix_map[prize_name]

            if not report_array[index+1][report_array_location]:
                report_array[index+1][report_array_location] = judge_sheet.participant.name
            else:
                report_array[index + 1][report_array_location] = report_array[index + 1][report_array_location] + " / " + judge_sheet.participant.name

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="FairTracker_Full_Report.csv"'

    writer = csv.writer(response)
    for row in report_array:
        writer.writerow(row)

    return response

def process_for_display(participants, entries, judge_sheets):
    # {
    #     data: [
    #         {
    #             "participant": {
    #                 "name"...
    #             },
    #             "entries": [
    #
    #             ],
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
            new_data["calculated"].update({
                "total_awarded": new_data["calculated"].get("total_awarded", 0) + calc_awards["prize_amount"]
            })

        return_object.append(new_data)

    return {
        "data": return_object
    }
