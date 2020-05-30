from django import forms
from .models import Fair

class FairForm(forms.ModelForm):
    class Meta:
        model = Fair
        fields = ["name", "city", "state"]