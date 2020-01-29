from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Create your views here.


def bidding(request):
	return HttpResponse('<h1>You are on bidding Page</h1>')


def login(request):
	return render(request, 'bidding/login.html')


def registration(request):
	return render(request, 'bidding/registration.html')
