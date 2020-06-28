from django.shortcuts import render

from fair.models import Fair


def index(request):
    fair_name = get_current_fair_name(request.user)
    context = {
        "current_fair_name": fair_name
    }
    return render(request, "catalog.html", context)


def get_current_fair_name(current_user):
    active_fair = Fair.objects.get(owner=current_user, active=True)
    return active_fair.name