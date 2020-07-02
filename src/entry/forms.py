
from django import forms
from .models import Entry

from entry.models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["participant", "catalog_item"]
