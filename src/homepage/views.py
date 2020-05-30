from django.shortcuts import render, redirect

def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'secure.html')
    else:
        return render(request, 'index.html')