# utilisateurs/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('account_panel/', views.user_panel, name='user_panel'),
    path('offer_panel/', views.offer_panel, name='offer_panel'),
    path('mailsent_panel/', views.mailsent_panel, name='mailsent_panel'),
    path('dashboard_panel/', views.dashboard_panel, name='dashboard_panel'),
    path('panel/', views.panel, name='panel'),

]