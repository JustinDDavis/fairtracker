"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('homepage.urls')),  # Landing page / Sign-in links
    path('fair/', include('fair.urls')),  # App to handle creation / Edit of Apps
    path('participant/', include('participant.urls')),  #
    path('catalog/', include('catalog.urls')),  #
    path('catalog-item/', include('catalog_item.urls')),  #
    path('entry/', include('entry.urls')),  #
    path('prize/', include('prize.urls')),  #
    path('judge-sheet/', include('judge_sheet.urls')),  #
    path('report/', include('report.urls')),  #
    path('admin/', admin.site.urls),  # Admin Portal
    path('', include('social_django.urls')),  # Auth0 Handlers /complete/auth0
    path('', include('auth0login.urls')),  # /login  and /logout
]

