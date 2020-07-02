
from django import forms
from .models import JudgeSheet


class JudgeSheetForm(forms.ModelForm):
    class Meta:
        model = JudgeSheet
        fields = ["participant", "prize"]
