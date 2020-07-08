from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models.functions import Lower

from fair.models import Fair
from catalog.models import Catalog

from .models import CatalogItem
from .forms import CatalogItemForm


def index(request):
    active_fair = Fair.objects.get(owner=request.user, active=True)
    catalog = Catalog.objects.get(fair=active_fair, active=True)
    catalog_items = CatalogItem.objects.filter(catalog=catalog)

    if request.method == "POST":
        form = CatalogItemForm(request.POST)
        if form.is_valid():
            form_object = form.save(commit=False)
            form_object.catalog = catalog
            form_object.save()
            messages.success(request, "Catalog Item Saved Successfully")
            return redirect("catalog_item_home")
        print(form.errors)
        messages.error(request, form.errors)
        return redirect("catalog_item_home")

    sort_column = request.GET.get('sort', '')
    if sort_column in ["name", "description"]:
        # sort=author
        catalog_items = catalog_items.order_by(Lower(sort_column))
    elif sort_column in ["-name", "-description"]:
        all_fairs = catalog_items.order_by(Lower(sort_column[1:]).desc())
    else:
        catalog_items = catalog_items.order_by(Lower("name"))

    context = {
        "active_catalog": catalog,
        "catalog_items": catalog_items
    }
    return render(request, "catalog_items.html", context)


def edit(request, catalog_item_id):
    catalog_item = CatalogItem.objects.get(pk=catalog_item_id)

    if request.method == "POST":
        form = CatalogItemForm(request.POST, instance=catalog_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Catalog Item Updated Successfully")
            return redirect("catalog_item_home")
        messages.error(request, form.errors)
        return redirect("catalog_item_edit")
    else:
        context = {
            "catalog_item": catalog_item
        }
        return render(request, "edit_catalog_items.html", context)


def delete(request, catalog_item_id):
    catalog_item = CatalogItem.objects.get(pk=catalog_item_id)
    catalog_item.delete()
    messages.success(request, "Catalog Item was deleted  successfully")
    return redirect('catalog_item_home')