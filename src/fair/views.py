
from django.shortcuts import render, redirect
from django.contrib import messages

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

    # fair_form = FairForm()
    context = {
        "current_user_fairs": all_fairs,
        # "form": fair_form
    }

    return render(request, "all_fairs.html", context)

def activate(request, fair_id):

    # TODO: COME BACK AND MAKE SURE THE CURRENT USER IS AN OWNER OF THIS FAIR
    fair = Fair.objects.get(pk=fair_id)

    fair.active = not fair.active
    fair.save()

    # Set all others to False active
    Fair.objects.filter(owner_id=request.user).exclude(pk=fair_id).update(active=False)

    return redirect('fair_home')


def edit(request, fair_id):
    fair = Fair.objects.get(pk=fair_id)

    if request.method == "POST":
        form = FairForm(request.POST, instance=fair)
        if form.is_valid():
            form.save()
            messages.success(request, "Fair Updated Successfully")
            return redirect("fair_home")
        messages.error(request, form.errors)
        return redirect("fair_edit")
    else:
        context = {
            "fair": fair
        }
        return render(request, "edit_fair.html", context)


def delete(request, fair_id):
    fair = Fair.objects.get(pk=fair_id)
    fair.delete()
    messages.success(request, "Fair was deleted  successfully")
    return redirect('fair_home')