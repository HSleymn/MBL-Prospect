from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime


def index(request):
    return redirect('login')  # 'login' est le nom de l'URL de ta page de connexion