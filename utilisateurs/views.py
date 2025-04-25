from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import SignupForm, CustomAuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Bienvenue, vous êtes connecté !")
            if user.is_superuser:  # ou user.is_staff
                return redirect('/admin/')  # Redirige vers le panel admin Django
            else:
                return redirect('user_panel')  # Redirige vers la page d'accueil ou une page spécifique
        else:
            messages.error(request, "Identifiants invalides.")
    else:
        form = AuthenticationForm()
    print(request.user)
    return render(request, 'users/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirige vers la page de login
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})
# Vue de déconnexion
# Pas besoin de créer une vue manuelle, Django le fait déjà avec LogoutView

def panel(request):
    user = request.user  # Récupère l'utilisateur connecté
    return render(request, 'users/panel.html', {'user': user})

@login_required
def user_panel(request):
    if not request.headers.get('HX-Request'):
        return redirect('panel')
    user = request.user  # Récupère l'utilisateur connecté
    return render(request, 'users/user_panel.html', {'user': user})

@login_required
def offer_panel(request):
    if not request.headers.get('HX-Request'):
        return redirect('panel')
    user = request.user  # Récupère l'utilisateur connecté
    return render(request, 'users/offer_panel.html', {'user': user})

def mailsent_panel(request):
    if not request.headers.get('HX-Request'):
        return redirect('panel')
    user = request.user  # Récupère l'utilisateur connecté
    return render(request, 'users/mailsent_panel.html', {'user': user})
def dashboard_panel(request):
    if not request.headers.get('HX-Request'):
        return redirect('panel')
    user = request.user  # Récupère l'utilisateur connecté
    return render(request, 'users/dashboard_panel.html', {'user': user})



