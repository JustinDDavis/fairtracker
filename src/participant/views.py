from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest


from fair.models import Fair

from .models import Participant
from .forms import ParticipantForm


def index(request):
    if not request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form_object = form.save(commit=False)

            current_user = request.user

            active_fair = Fair.objects.get(owner=current_user, active=True)

            form_object.fair = active_fair

            form_object.save()
            messages.success(request, "Request was saved successfully")
            return redirect("participant_home")

        messages.error(request, form.errors)
        return HttpResponseBadRequest("Invalid form")

    current_user = request.user
    active_fair = Fair.objects.get(owner=current_user, active=True)

    all_participants = Participant.objects.filter(fair=active_fair)

    context = {
        "current_user_participants": all_participants
    }
    return render(request, "all_participants.html", context)


def delete(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)
    participant.delete()
    messages.success(request, "Participant was deleted  successfully")
    return redirect('participant_home')