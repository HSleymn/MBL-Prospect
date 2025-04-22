from django.contrib import admin
from django.urls import path, include
from django.views.defaults import server_error

from commandes.views import get_offer_price
from prospectWebApp.views import index


path('get_offer_price/<int:offer_id>/', get_offer_price, name='get_offer_price'),