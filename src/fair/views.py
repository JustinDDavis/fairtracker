
from django.shortcuts import render, redirect
from django.contrib import messages

from django.db.models.functions import Lower

from .models import Fair
from .forms import FairForm


def index(request):
    if not request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = FairForm(request.POST)
        if form.is_valid():

            form_object = form.save(commit=False)

            current_user = request.user
            form_object.owner = current_user

            form_object.save()
            messages.success(request, "Request was saved successfully")
            return redirect("fair_home")

        messages.error(request, form.errors)

    all_fairs = Fair.objects.filter(owner_id=request.user)

    sort_column = request.GET.get('sort', '')
    if sort_column in ["name", "city", "state"]:
        # sort=author
        all_fairs = all_fairs.order_by(Lower(sort_column))
    elif sort_column in ["-name", "-city", "-state"]:
        all_fairs = all_fairs.order_by(Lower(sort_column[1:]).desc())
    else:
        all_fairs = all_fairs.order_by(Lower("name"))

    context = {
        "current_user_fairs": all_fairs,
    }

    return render(request, "test.html", context)


def activate(request, fair_id):
    # TODO: COME BACK AND MAKE SURE THE CURRENT USER IS AN OWNER OF THIS FAIR
    fair = Fair.objects.get(pk=fair_id)

    if fair.owner != request.user:
        # Fair is not owned by this person
        return redirect('fair_home')

    fair.active = not fair.active
    fair.save()

    # Set all others to False active
    Fair.objects.filter(owner_id=request.user).exclude(pk=fair_id).update(active=False)

    return redirect('fair_home')


def edit(request, fair_id):
    fair = Fair.objects.get(pk=fair_id)

    if fair.owner != request.user:
        # print("Edit - Fair is not owned by this person")
        return redirect('fair_home')

    if request.method == "POST":
        form = FairForm(request.POST, instance=fair)
        if form.is_valid():
            form.save()
            messages.success(request, "Fair Updated Successfully")
            return redirect("fair_home")
        messages.error(request, form.errors)
        return redirect("fair_home")
    else:
        context = {
            "fair": fair
        }
        return render(request, "edit_fair.html", context)
#
#
# def delete(request, fair_id):
#     fair = Fair.objects.get(pk=fair_id)
#     if fair.owner != request.user:
#         print("Delete - Fair is not owned by this person")
#         return redirect('fair_home')
#
#     fair.delete()
#     messages.success(request, "Fair was deleted  successfully")
#     return redirect('fair_home')