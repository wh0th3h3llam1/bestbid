# from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage		# for saving images
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
import datetime
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
# @redirect_authenticated_user(redirect_field_name=REDIRECT_FIELD_NAME, redirect_url=settings.LOGIN_REDIRECT_URL)
def login(request):
	'''
	if request.session.user_type == 'seller':
		return render(request, 'bidding/.html')
	if request.session.user_type == 'buyer':
		return render(request, 'bidding/login.html')
	'''
	return render(request, 'bidding/login.html')


def buyer_login(request):
	form = BuyerLoginForm()
	context = {'form' : form}
	return render(request, 'bidding/buyer_login.html', context)


def seller_login(request):
	form = SellerLoginForm()
	context = {'form' : form}
	return render(request, 'bidding/seller_login.html', context)


# Registration
def registration(request):

	context = {}
	return render(request, 'bidding/registration.html', context)


def buyer_reg(request):
	form = BuyerForm()

	if request.method == 'POST':
		form = BuyerForm(request.POST)
		if	form.is_valid():
			form.save()
			unm = form.cleaned_data.get('name')
			messages.success(request, 'Buyer Profile Created Successfully for ' + unm)
			return render(request, 'bidding/login.html')

	context = {'form' : form}
	return render(request, 'bidding/buyer_reg.html', context)


def seller_reg(request):

	form = SellerForm()

	if request.method == 'POST':
		form = SellerForm(request.POST)
		if	form.is_valid():
			form.save()
			unm = form.cleaned_data.get('name')
			messages.success(request, 'Seller Profile Created Successfully for ' + unm)
			return render(request, 'bidding/login.html')


	context = {'form' : form}
	return render(request, 'bidding/seller_reg.html', context)


# Dashboard
def buyer_dashboard(request):
	if request.method == 'POST':
		form = BuyerLoginForm(request.POST)
		req_email = request.POST.get('email')
		req_password = request.POST.get('password')
		try:
			user = Buyer.objects.get(Q(email=req_email) & Q(password=req_password))
			auctions = Auction.objects.all()
			context = {
				'user' : user,
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
			return render(request, 'bidding/login.html')

	elif request.session.get('id'):
			user_id = request.session.get('id')
			user = get_object_or_404(Buyer, id=user_id)
			auctions = Auction.objects.all()
			context = {
				'user' : user,
				'auctions' : auctions,
				'loggedIn' : 'loggedIn',
				'user_type' : 'buyer',
			}
			context.update(csrf(request))
			request.session['id'] = user.id
			request.session['name'] = user.name
			request.session['user_type'] = 'buyer'
			return render(request, 'bidding/buyer_dashboard.html', context)
	else:
		return render(request, 'bidding/login.html')


def seller_dashboard(request):
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
			return render(request, 'bidding/login.html')

	elif request.session.get('id'):
			user_id = request.session.get('id')
			user = get_object_or_404(Seller, id=user_id)
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
	else:
		return render(request, 'bidding/login.html')


# @login_required(login_url='login')
def profile(request, user_type, user_id, edit=None, change_password=None):
	user_id = request.POST.get('user_id')
	user_type = request.POST.get('user_type')

	if user_type == 'seller':
		user = get_object_or_404(Seller, id=user_id)
		user_assets = Asset.objects.filter(Q(seller=user.id))
		assets_sold = AuctionedAsset.objects.filter(Q(seller=user.id))
		context = {
			'user' : user,
			'user_assets' : user_assets,
			'assets_sold' : assets_sold,
		}
	elif user_type == 'buyer':
		user = get_object_or_404(Buyer, id=user_id)
		assets_bought = AuctionedAsset.objects.filter(Q(buyer=user.id))
		context = {
			'user' : user,
			'assets_bought' : assets_bought,
		}
	else:
		return HttpResponse('Profile Not Found for user type')

	if change_password == 'change_password':
		context = {
			'user' : user,
		}
		return render(request, 'bidding/change_password.html', context)
	if edit == 'edit':
		form = EditProfileForm(instance=user)
		context = {
			'user' : user,
			'form' : form
		}
		return render(request, 'bidding/edit_profile.html', context)
	else:
		return render(request, 'bidding/show_profile.html', context)


def edit_profile(request):
	name = request.POST.get('name')
	email = request.POST.get('email')
	oldpwd = request.POST.get('oldpwd')
	newpwd1 = request.POST.get('newpwd1')
	newpwd2 = request.POST.get('newpwd2')
	user_id = request.POST.get('user_id')
	user_type = request.POST.get('user_type')

	if user_type == 'seller':
		user = get_object_or_404(Seller, id=user_id)
	elif user_type == 'buyer':
		user = get_object_or_404(Buyer, id=user_id)
	else:
		return HttpResponse('Not Found')
	# user.name = 



	messages.success(request, "Profile Updated Successfully")
	return render(request, 'bidding/show_profile.html', context)
	

# Bid
def bid(request):
	'''
	try:
		if request.session.user_type == 'buyer':
			auctioned = AuctionedAsset.objects.all()
			assets = Asset.objects.exclude(sold__in=auctioned)
			# assets = Asset.objects.get(sold=False)
			print(assets)
			context = { 'assets' : assets}
			return render(request, 'bidding/bid.html', context)
		else:
			messages.error(request, "Please Login as using a Buyer account.")
			return render(request, 'bidding/buyer_login.html', context)
	except:
		messages.error(request, "Please Login to Continue.")
		return render(request, 'bidding/login.html')
	'''
	auctioned = AuctionedAsset.objects.all()
	assets = Asset.objects.exclude(sold__in=auctioned)
	# assets = Asset.objects.get(sold=False)
	now = datetime.datetime.now()
	allow_bid = False
	if now.hour > 10 and now.hour < 12:
		allow_bid = True
	context = { 'assets' : assets, 'allow_bid' : allow_bid }
	return render(request, 'bidding/bid.html', context)


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
		user_id = request.POST.get('id')
		user_type = request.POST.get('user_type')
	
		name = request.POST.get('name')
		baseprice = request.POST.get('baseprice')
		category = request.POST.get('selectedOption')
		'''
		l = []
		for f in request.FILES.get('image'):
			myImagename = f.name
			l.append(myImagename)
			print(myImagename)
		print(l)
		print()
		print()
		'''
		image = request.FILES['image']
		description = request.POST.get('description')
		user_name = request.POST.get('user_name')
		
		seller_instance = get_object_or_404(Seller, name=user_name)
		# print(name)
		# print(baseprice)
		# print(category)
		# print(image)
		# print(description)
		# print(user_name)

		fs = FileSystemStorage()
		image_name = fs.save(image.name, image)
		print(image_name)
		asset = Asset.objects.create(
			name=name,
			baseprice=baseprice,
			category=category,
			image=image_name,
			details=description,seller=seller_instance,
			sold=False)
		asset.save()
		user = get_object_or_404(Seller, id=id)
		context = {
			'user' : user,
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
	}
	return render(request, 'bidding/index.html', context)


def edit_asset(request):
	if request.method == 'POST':
		user_id = request.POST.get('id')
		user_type = request.POST.get('user_type')
	
		name = request.POST.get('name')
		baseprice = request.POST.get('baseprice')
		category = request.POST.get('selectedOption')
		image = request.FILES['image']
		description = request.POST.get('description')

		seller_instance = get_object_or_404(Seller, id=user_id)
		
		fs = FileSystemStorage()
		image_name = fs.save(image.name, image)

		asset = Asset.objects.create(
			name=name,
			baseprice=baseprice,
			category=category,
			image=image_name,
			details=description,seller=seller_instance,
			sold=False)
		asset.save()
		user = get_object_or_404(Seller, id=id)
		context = {
			'user' : user,
		}
		return render(request, 'bidding/seller_dashboard.html', context)


# Asset Page
def asset(request, id, edit=None):
	if request.method == 'POST':
		if request.POST.get('delete'):
			try:
				Asset.objects.filter(id=id).delete()
				context = { 'success' : 'success'}
				return render(request, 'bidding/delete.html', context)
			except:
				context = { 'failed' : 'failed'}
				return render(request, 'bidding/delete.html', context)
		if request.POST.get('edit'):
			asset = get_object_or_404(Asset, id=id)
			context = {
				'asset' : asset,
				}
			return render(request, 'bidding/edit_asset.html', context)
	# try:
	asset = get_object_or_404(Asset, id=id)
	now = datetime.datetime.now()
	allow_bid = False
	if now.hour > 10 and now.hour < 12:
		allow_bid = True
	context = {
		'asset' : asset,
		'now' : now,
		'allow_bid' : allow_bid
	}
	return render(request, 'bidding/asset.html', context)
	# except:
	# 	return HttpResponse('<h1 style="text-align:center;">Asset Not Found</h1>')


def reset_password(request):
	if request.method == 'POST':
		pass
		# user_type = request.POST.get('user_type')
		# user_id = request.POST.get('id')
		# pwd1 = request.POST.get('pwd1')
		# if user_type == 'seller':
		# 	user = get_object_or_404(Seller, id=user_id)
		# else user_type == 'buyer':
		# 	user = get_object_or_404(Buyer, id=user_id)
		# user.password = pwd1
		# user.save()
		# context = {
		# 	'user' : user,
		# }

# Logout
def logout(request):
	for key in list(request.session.keys()):
		del request.session[key]
	messages.success(request, "User Logged Out Successfully")
	return render(request, 'bidding/login.html')