# from django.contrib.admin.views.decorators import staff_member_required
# from django.core.files.storage import FileSystemStorage		# for saving images
# from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from urllib.parse import urlencode
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
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
	# context = {'seller_form' : seller_form, 'buyer_form' : buyer_form}
	context = {}
	return render(request, 'bidding/login.html', context)


def buyer_login(request):
	if request.method == 'POST':
		form = BuyerLoginForm(request.POST)
		req_email = request.POST.get('email')
		req_password = request.POST.get('password')
		try:
			user = Buyer.objects.get(Q(email=req_email) & Q(password=req_password))
			last_five = AuctionedAsset.objects.all().order_by('id')[:5]
			auctions = Auction.objects.all()
			context = {
				'user' : user,
				'last_five' : last_five,
				'auctions' : auctions,
				'loggedIn' : 'loggedIn',
				'user_type' : 'buyer',
			}
			context.update(csrf(request))
			request.session['id'] = user.id
			request.session['name'] = user.name
			request.session['user_type'] = 'buyer'
			return render(request, 'bidding/buyer_dashboard.html', context)
		except Buyer.DoesNotExist:
			messages.error(request, 'Incorrect Credentials')

	form = BuyerLoginForm()
	context = {'form' : form}
	return render(request, 'bidding/buyer_login.html', context)


def seller_login(request):
	if request.method == 'POST':
		form = SellerLoginForm(request.POST)
		req_email = request.POST.get('email')
		req_password = request.POST.get('password')
		try:
			user = Seller.objects.get(Q(email=req_email) & Q(password=req_password))
			auctions = Auction.objects.all()
			context = {
				'user' : user,
				'auctions' : auctions,
				'loggedIn' : 'loggedIn',
				'user_type' : 'seller',
			}
			context.update(csrf(request))
			request.session['id'] = user.id
			request.session['name'] = user.name
			request.session['user_type'] = 'seller'
			return render(request, 'bidding/seller_dashboard.html', context)
		except Seller.DoesNotExist:
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
# @login_required(login_url='buyer_login')
def buyer_dashboard(request):
	context = {}
	return render(request, 'bidding/buyer_dashboard.html', context)


# @login_required(login_url='seller_login')
def seller_dashboard(request):
	context = {}
	return render(request, 'bidding/seller_dashboard.html', context)


# @login_required(login_url='login')
def profile(request, user_type, user_id, edit=None):
	user_id = request.POST.get('user_id')
	user_type = request.POST.get('user_type')

	if user_type == 'seller':
		user = get_object_or_404(Seller, id=user_id)
	elif user_type == 'buyer':
		user = get_object_or_404(Buyer, id=user_id)
	else:
		return HttpResponse('Not Found')
	context = {
		'user' : user,
	}
	if edit == 'edit':
		return render(request, 'bidding/edit_profile.html', context)
	else:
		return render(request, 'bidding/show_profile.html', context)


# Bid
def bid(request):
	context = { 'bid' : 'bid'}
	return render(request, 'bidding/bid.html')#, context)


# Search for Assets
def search(request):
	if request.method == 'POST':
		query = request.POST.get('search_query')
		if query:
			# If search has query
			results = Asset.objects.filter(Q(name__icontains=query) | Q(category__icontains=query))

			if results:
				# If results are found
				context = {'search_results' : results, 'query' : query, 'search' : 'search'}
				return render(request, 'bidding/search.html', context)
			else:
				# If no results are found
				context = {'no_results' : 'no_results', 'search' : 'search'}
				return render(request, 'bidding/search.html', context)
		else:
			# If search query is empty
			return render(request, 'bidding/search.html')
	else:
		return render(request, 'bidding/search.html')


# @login_required(login_url='login')
def upload(request):
	if request.method == 'POST':
		form = AssetForm(request.POST)
		if	form.is_valid():	
			user_id = request.POST.get('user_id')
			user = get_object_or_404(Seller, id=user_id)
			context = {
				'user' : user,
				'loggedIn' : 'loggedIn',
			}
			return render(request, 'bidding/seller_dashboard.html', context)
			
	form = AssetForm()
	user_id = request.GET.get('user_id')
	user = get_object_or_404(Seller, id=user_id)
	context = {'form' : form, 'user' : user}
	return render(request, 'bidding/upload.html', context)


# Index
def index(request):
	assets = Asset.objects.all()
	last_five = AuctionedAsset.objects.all().order_by('id')[:5]
	auctions = Auction.objects.all()
	context = {
		'last_five' : last_five,
		'auctions' : auctions,
		'assets' : assets,
		'home' : 'home',
	}
	return render(request, 'bidding/index.html', context)


# Asset Page
def asset(request, id):
	try:
		asset = get_object_or_404(Asset, id=id)
	except:
		return HttpResponse('Asset Not Found')
	context = {
		'asset' : asset,
	}
	return render(request, 'bidding/asset.html', context)


# Logout
def logout(request):
	for key in list(request.session.keys()):
		del request.session[key]
	messages.success(request, "User Logged Out Successfully")
	return render(request, 'bidding/login.html')