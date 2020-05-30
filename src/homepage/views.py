from django.shortcuts import render, redirect
import json

def index(request):
    user = request.user
    if user.is_authenticated:
        user = request.user
        auth0user = user.social_auth.get(provider='auth0')
        userdata = {
            'user_id': auth0user.uid,
            'name': user.first_name,
            'picture': auth0user.extra_data['picture'],
            'email': auth0user.extra_data['email'],
        }
        return render(request, 'secure.html', {
            'auth0User': auth0user,
            'userdata': json.dumps(userdata, indent=4)
        })

    else:
        return render(request, 'index.html')