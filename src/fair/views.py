
from django.shortcuts import render


def index(request):
    return render(request, "all_fairs.html", {
        "current_user_fairs": [{
            'name':'Fair 1'
        }]
    })