from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from datetime import datetime


def index(request):
    return render(request, 'index.html', context={"prenom" : request.user.lastname + " "+request.user.firstname , "date" : datetime.today()})