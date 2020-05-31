from django.shortcuts import render, redirect
import json

from fair.models import Fair

def index(request):

    return render(request, 'index.html', {
        'user_is_authentication': request.user.is_authenticated
    })

def user_homepage(request):
    if not request.user.is_authenticated:
        return redirect('home')
    

    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }

    all_fair_items = Fair.objects.all()
    
    return render(request, 'user_homepage.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4),
        'fairs': all_fair_items
    })