
from django.shortcuts import render, redirect

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

            print("ENd")
            form_object.save()
            return redirect("home")

    all_fairs = Fair.objects.all()

    fair_form = FairForm()
    context = {
        "current_user_fairs": all_fairs,
        "form": fair_form
    }

    return render(request, "all_fairs.html", context)
