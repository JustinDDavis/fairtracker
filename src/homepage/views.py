from django.shortcuts import render, redirect
from fair.models import Fair


def index(request):
    if request.user.is_authenticated:
        return redirect('user_homepage')

    return render(request, 'index.html', {
        'user_is_authentication': request.user.is_authenticated
    })


def user_homepage(request):
    if not request.user.is_authenticated:
        return redirect('home')

    all_fair_items = Fair.objects.filter(owner=request.user)
    
    return render(request, 'user_homepage.html', {
        'fairs': all_fair_items
    })