from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.functions import Lower

from fair.models import Fair
from catalog.models import Catalog
from .models import Prize

from .forms import PrizeForm

def index(request):
    active_fair = Fair.objects.get(owner=request.user, active=True)
    current_catalog = Catalog.objects.get(fair=active_fair, active=True)
    print(current_catalog)

    if request.method == "POST":
        form = PrizeForm(request.POST)
        if form.is_valid():
            form_object = form.save(commit=False)
            form_object.catalog = current_catalog
            form_object.save()
            messages.success(request, "Prize Saved Successfully")
            return redirect("prize_home")
        print(form.errors)
        messages.error(request, form.errors)
        return redirect("prize_home")

    prizes = Prize.objects.filter(catalog=current_catalog).extra(
        select={'cast_amount': 'CAST(amount AS INTEGER)'}
    )

    sort_column = request.GET.get('sort', '')
    if sort_column in ["name", "description"]:
        # sort=author
        prizes = prizes.order_by(Lower(sort_column))
    elif sort_column in ["-name", "-description"]:
        prizes = prizes.order_by(Lower(sort_column[1:]).desc())
    elif sort_column in ["amount", "-amount"]:
        if sort_column[0] == "-":
            prizes = prizes.order_by("-cast_amount")
        else:
            prizes = prizes.order_by("cast_amount")
    else:
        prizes = prizes.order_by(Lower("name"))

    context = {
        "prizes": prizes,
        "catalog": current_catalog
    }

    return render(request, "prize.html", context)

def edit(request, prize_id):
    prize = Prize.objects.get(pk=prize_id)

    if request.method == "POST":
        form = PrizeForm(request.POST, instance=prize)
        if form.is_valid():
            form.save()
            messages.success(request, "Prize Updated Successfully")
            return redirect("prize_home")
        messages.error(request, form.errors)
        return redirect("prize_edit")
    else:
        context = {
            "prize": prize
        }
        return render(request, "edit_prize.html", context)




def delete(request, prize_id):
    prize = Prize.objects.get(pk=prize_id)
    prize.delete()
    messages.success(request, "Prize was deleted  successfully")
    return redirect('prize_home')
