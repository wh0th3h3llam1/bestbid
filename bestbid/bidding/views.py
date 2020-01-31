from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Create your views here.


def login(request):
	return render(request, 'bidding/login.html')


def registration(request):
	return render(request, 'bidding/registration.html')


def index(request):
	STATIC_URL = settings.STATIC_URL
	print(STATIC_URL)
	context = {'su' : STATIC_URL}
	return render(request, 'bidding/index.html', context)


def agency(request):
	return render(request, 'bidding/agency.html')
