from django.shortcuts import render, redirect
from fair.models import Fair
from participant.models import Participant
from catalog.models import Catalog
from entry.models import Entry
from prize.models import Prize
from judge_sheet.models import JudgeSheet

def index(request):
    if request.user.is_authenticated:
        return redirect('user_homepage')

    return render(request, 'index.html', {
        'user_is_authentication': request.user.is_authenticated
    })


def user_homepage(request):
    if not request.user.is_authenticated:
        return redirect('home')

    all_fair_items = Fair.objects.filter(owner=request.user)

    active_fair = Fair.objects.get(owner=request.user, active=True)

    participant_count = len(Participant.objects.filter(fair=active_fair))
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    entry_count = len(Entry.objects.filter(catalog_item__catalog=catalog))

    prize_money_awarded = 0
    for judge_sheet in JudgeSheet.objects.filter(catalog_item__catalog=catalog):
        prize_money_awarded += int(judge_sheet.prize.amount)
    
    return render(request, 'user_homepage.html', {
        'fairs': all_fair_items,
        'participant_count': participant_count,
        'entry_count': entry_count,
        'prize_money_awarded': prize_money_awarded
    })