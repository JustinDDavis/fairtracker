
from django import forms
from .models import Participant

class ParticipantForm(forms.ModelForm):
    static_participant_id = forms.CharField(required=False)

    class Meta:
        model = Participant
        fields = ["name", "email", "city", "static_participant_id"]