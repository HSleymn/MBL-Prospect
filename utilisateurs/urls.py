# utilisateurs/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('panel/', views.user_panel, name='user_panel'),

    ]