# from django.core.files.storage import FileSystemStorage		# for saving images
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode
from .models import *
from .forms import *

# Create your views here.


# Admin - Login
def adminLogin(request):
	print("In adminLogin")
	if request.method == 'POST':
		print("In POST")
		req_email = request.POST.get('adminEmail')
		req_password = request.POST.get('adminPassword')
		admin_email = 'admin@gmail.com'
		admin_pwd = 'adminpass'
		if req_email == admin_email and req_password == admin_pwd:
			# c = {}	
			# c.update(csrf(request))
			# return redirect('home', c)#, context)
			# return redirect('home', c, context)

			assets = Asset.objects.all()
			sellers = Seller.objects.all()
			buyers = Buyer.objects.all()
			auctions = Auction.objects.all()
			auctionedAssets = AuctionedAsset.objects.all()
			
			context = {
				'assets' : assets,
				'sellers' : sellers,
				'buyers' : buyers,
				'auctions' : auctions,
				'auctionedAssets' : auctionedAssets,
			}
			context.update(csrf(request))

			return render(request, 'bidding/home.html', context)
		else:
			return render(request, 'bidding/adminLogin.html')	

	return render(request, 'bidding/adminLogin.html')	

# Admin - Home Page
@login_required(login_url='adminLogin')
def home(request):

	assets = Asset.objects.all()
	sellers = Seller.objects.all()
	buyers = Buyer.objects.all()
	auctions = Auction.objects.all()
	auctionedAssets = AuctionedAsset.objects.all()
	
	context = {
		'assets' : assets,
		'sellers' : sellers,
		'buyers' : buyers,
		'auctions' : auctions,
		'auctionedAssets' : auctionedAssets,
	}
	return render(request, 'bidding/home.html', context)


# User Login 
def login(request):

	buyer_form = BuyerLoginForm()
	seller_form = SellerLoginForm()
	context = {'seller_form' : seller_form, 'buyer_form' : buyer_form}
	return render(request, 'bidding/login.html', context)


def buyer_login(request):
	if request.method == 'POST':
		form = BuyerLoginForm(request.POST)
		
		req_email = request.POST.get('email')
		req_password = request.POST.get('password')
		user = Buyer.objects.filter(Q(email=req_email) & Q(password=req_password))
		
		if user:
			c = {}
			c.update(csrf(request))
			context = {'c' : c, 'loggedIn' : 'loggedIn'}
			messages.success(request, 'Buyer Logged In Successfully')

			return render(request, 'bidding/buyer_dashboard.html', context)
		else:
			messages.error(request, 'Incorrect Credentials')

	form = BuyerLoginForm()
	context = {'form' : form}
	
	return render(request, 'bidding/buyer_login.html', context)


def seller_login(request):
	if request.method == 'POST':
		form = SellerLoginForm(request.POST)
		
		req_email = request.POST.get('email')
		req_password = request.POST.get('password')
		user = Seller.objects.filter(Q(email=req_email) & Q(password=req_password))
		
		if user:
			# print(user.id)
			c = {}
			c.update(csrf(request))
			context = {'c' : c, 'loggedIn' : 'loggedIn'}
			# messages.success(request, 'Seller Logged In Successfully')
			return redirect('seller_dashboard', permanent=True)
			# return render(request, 'bidding/seller_dashboard.html', context)
		else:
			messages.error(request, 'Incorrect Credentials')

	form = SellerLoginForm()
	context = {'form' : form}
	return render(request, 'bidding/seller_login.html', context)


# Registration
def registration(request):

	context = {}
	return render(request, 'bidding/registration.html', context)


def buyer_reg(request):

	form = BuyerRegistrationForm()

	if request.method == 'POST':
		form = BuyerRegistrationForm(request.POST)
		if	form.is_valid():
			form.save()
			unm = form.cleaned_data.get('name')
			messages.success(request, 'Buyer Profile Created Successfully for ' + unm)
			# return redirect('login')
			return render(request, 'bidding/login.html')

	context = {'form' : form}
	return render(request, 'bidding/buyer_reg.html', context)


def seller_reg(request):

	form = SellerRegistrationForm()

	if request.method == 'POST':
		form = SellerRegistrationForm(request.POST)
		if	form.is_valid():
			form.save()
			unm = form.cleaned_data.get('name')
			messages.success(request, 'Seller Profile Created Successfully for ' + unm)
			# return redirect('login')
			return render(request, 'bidding/login.html')

			
	context = {'form' : form}
	return render(request, 'bidding/seller_reg.html', context)


# Dashboard
@login_required(login_url='login')
def buyer_dashboard(request, user):
	print(user)
	context = {}
	return render(request, 'bidding/buyer_dashboard.html', context)


@login_required(login_url='login')
def seller_dashboard(request, user):
	print(user)
	context = {}
	return render(request, 'bidding/seller_dashboard.html', context)


def index(request):
	assets = Asset.objects.all()

	context = {'assets' : assets}
	return render(request, 'bidding/index.html', context)


# Logout
def logoutUser(request):
	for key in list(request.session.keys()):
		del request.session[key]
	messages.success(request, "User Logged Out Successfully")
	return render(request, 'bidding/login.html')
	# return redirect('login')
	# return HttpResponseRedirect('login')