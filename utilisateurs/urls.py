# utilisateurs/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('account_panel/', views.user_panel, name='user_panel'),
    path('logout/', views.logout_view, name='logout_view'),
    path('offer_panel/', views.offer_panel, name='offer_panel'),
    path('mailsent_panel/', views.mailsent_panel, name='mailsent_panel'),
    path('dashboard_panel/', views.dashboard_panel, name='dashboard_panel'),
    path('panel/', views.panel, name='panel'),
    path('payment/<int:cart_id>/', views.payment_view, name='payment'),
    path('confirm_payment/<int:cart_id>/', views.confirm_payment_view, name='confirm_payment'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:offer_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:offer_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('panier/update/', views.update_cart, name='update_cart'),
    path('tracking/<uuid:mail_id>/', views.tracking_pixel, name='tracking_pixel'),
]