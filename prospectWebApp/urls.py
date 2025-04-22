"""
URL configuration for prospectWebApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include
from django.views.defaults import server_error
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from prospectWebApp.views import index
def custom_login_view(request):
    # Redirige l'utilisateur directement vers la page de login de Google
    return redirect('socialaccount_login', provider='google')

urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('utilisateurs/', include('utilisateurs.urls')),  # ← c'est bon
    path('utilisateurs/accounts/', include('allauth.urls')),  # ← obligatoire pour allauth
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


