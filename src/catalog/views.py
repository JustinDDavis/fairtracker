from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest

from .forms import CatalogForm
from .models import Catalog
from fair.models import Fair


def index(request):
    if not request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CatalogForm(request.POST)
        if form.is_valid():
            form_object = form.save(commit=False)
            form_object.fair = get_current_fair(request.user)
            form_object.save()

            messages.success(request, "Catalog Saved Successfully")
            return redirect("catalog_home")
        messages.error(request, form.errors)
        return redirect("catalog_home")

    fair = get_current_fair(request.user)
    all_catalogs = get_current_catalogs(fair)
    context = {
        "current_fair_name": fair.name,
        "all_catalogs": all_catalogs
    }
    return render(request, "catalog.html", context)

def activate(request, catalog_id):
    # TODO: COME BACK AND MAKE SURE THE CURRENT USER IS AN OWNER OF THIS Catalog
    catalog = Catalog.objects.get(pk=catalog_id)
    catalog.active = not catalog.active
    catalog.save()
    return redirect('catalog_home')

def edit(request, catalog_id):
    catalog = Catalog.objects.get(pk=catalog_id)

    if request.method == "POST":
        form = CatalogForm(request.POST, instance=catalog)
        if form.is_valid():
            form.save()
            messages.success(request, "Catalog Updated Successfully")
            return redirect("catalog_home")
        messages.error(request, form.errors)
        return redirect("catalog_edit")
    else:
        context = {
            "catalog": catalog
        }
        return render(request, "edit_catalog.html", context)


def delete(request, catalog_id):
    catalog = Catalog.objects.get(pk=catalog_id)
    catalog.delete()
    messages.success(request, "Catalog was deleted  successfully")
    return redirect('catalog_home')


def get_current_fair(current_user):
    active_fair = Fair.objects.get(owner=current_user, active=True)
    return active_fair


def get_current_catalogs(active_fair):
    return Catalog.objects.filter(fair=active_fair)