from django import forms
from .models import CatalogItem

from catalog.models import Catalog

class CatalogItemForm(forms.ModelForm):
    class Meta:
        model = CatalogItem
        fields = ["name", "description"]
