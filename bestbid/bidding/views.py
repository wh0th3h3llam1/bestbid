# from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage		# for saving images
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from bestbid.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib import messages
from urllib.parse import urlencode
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from .models import *
from .forms import *
import datetime, random

from .tasks import send_email_task


# Create your views here.


# Admin - Login
def manager(request):
	if request.method == 'POST':
		req_email = request.POST.get('managerEmail')
		req_password = request.POST.get('managerPassword')
		manager_email = 'manager@bestbid.com'
		manager_pwd = 'managerpass'
		if req_email == manager_email and req_password == manager_pwd:
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
			return render(request, 'bidding/manager.html')

	return render(request, 'bidding/manager.html')


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
			
			assets_bought = AuctionedAsset.objects.filter(Q(buyer=user.id))
			auctioned = AuctionedAsset.objects.all()
			assets = Asset.objects.exclude(sold__in=auctioned)[:3]
			context = {
				'user' : user,
				'assets_bought' : assets_bought,
				'assets' : assets,
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

			assets_bought = AuctionedAsset.objects.filter(Q(buyer=user.id))
			auctioned = AuctionedAsset.objects.all()
			assets = Asset.objects.exclude(sold__in=auctioned)[:3]
			context = {
				'user' : user,
				'assets_bought' : assets_bought,
				'assets' : assets,
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
			assets = Asset.objects.filter(Q(seller=user.id))
			assets_sold = AuctionedAsset.objects.filter(Q(seller=user.id))
			context = {
				'user' : user,
				'assets' : assets,
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
			assets = Asset.objects.filter(Q(seller=user.id))
			context = {
				'user' : user,
				'assets' : assets,
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
			'assets_bought' : assets_bought
		}
	else:
		return HttpResponse('Profile Not Found for user type')

	if change_password == 'change_password':
		if request.POST.get('check_pwd'):
			print('password changed')
			pass
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
	auctioned = AuctionedAsset.objects.all()
	assets = Asset.objects.exclude(sold__in=auctioned)

	now = datetime.datetime.now()
	print(now.hour)
	# Allow bid only Between 10 AM and 1 PM
	allow_bid = False
	if now.hour in range(10, 14):
		allow_bid = True

	about_to_end = False
	# About to End
	if	now.hour == 12 and now.minute > 50:
		about_to_end = True

	# allow_bid = True # Temporary
	context = {
		'assets' : assets,
		'allow_bid' : allow_bid,
		'about_to_end' : about_to_end
	}
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
		user_id = request.POST.get('user_id')
		user_type = request.POST.get('user_type')
		name = request.POST.get('name')
		baseprice = request.POST.get('baseprice')
		category = request.POST.get('selectedOption')
		image = request.FILES['image']
		description = request.POST.get('description')
		user_name = request.POST.get('user_name')
		
		seller_instance = get_object_or_404(Seller, name=user_name)

		fs = FileSystemStorage()
		image_name = fs.save(image.name, image)
		print(image_name)
		asset = Asset.objects.create(
			name=name,
			baseprice=baseprice,
			category=category,
			image=image_name,
			details=description,
			seller=seller_instance,
			sold=False)
		asset.save()
		user = get_object_or_404(Seller, id=user_id)
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
	last_five = AuctionedAsset.objects.all().order_by('id')[:5]
	auctioned = AuctionedAsset.objects.all()
	assets = Asset.objects.exclude(sold__in=auctioned)

	context = {
		'last_five' : last_five,
		'assets' : assets,
	}
	return render(request, 'bidding/index.html', context)


# Edit Asset
def edit_asset(request):
	if request.method == 'POST':
		user_id = request.session.get('id')
		asset_id = request.POST.get('asset_id')

		name = request.POST.get('name')
		baseprice = request.POST.get('baseprice')
		category = request.POST.get('selectedOption')
		description = request.POST.get('description')

		seller_instance = get_object_or_404(Seller, id=user_id)
		
		asset = Asset.objects.get(Q(id=asset_id))
		
		asset.name=name
		asset.baseprice=baseprice
		asset.category=category
		asset.details=description

		asset.save()
		user = get_object_or_404(Seller, id=user_id)
		context = {
			'user' : seller_instance,
		}
		return render(request, 'bidding/seller_dashboard.html', context)


# Asset Page
def asset(request, id, edit=None):
	# Current Time
	now = datetime.datetime.now()
	
	# Allow Bid only Between 10 AM and 1 PM
	allow_bid = False
	if now.hour > 10 and now.hour < 13:
		allow_bid = True

	# About to End
	about_to_end = False
	if	now.hour == 12 and now.minute > 50:
		about_to_end = True

	# End Bid
	if now.hour == 12 and now.minute >= 59:
		end = True
		live_auction_status = LiveAuction.objects.filter(Q(asset=id)).order_by('-price')
		sold_to = live_auction_status[0]
		print("sold for : ", sold_to.price)
		print("sold to : ", sold_to.buyer)
		asset = get_object_or_404(Asset, id=id)
		asset.sold = True # Mark as sold
		asset.save()
		asset_instance = get_object_or_404(Asset, id=asset.id)
		seller_instance = get_object_or_404(Seller, id=asset.seller.id)
		buyer_instance = get_object_or_404(Buyer, id=sold_to.buyer.id)
		auction = Auction.objects.create()
		auction.save()

		auctioned = AuctionedAsset.objects.create(
			auction_id=auction,
			asset=asset_instance,
			seller=seller_instance,
			buyer=buyer_instance,
			category=asset_instance.category,
			price=sold_to.price
		)
		auctioned.save()

		# LiveAuction.objects.all().delete()

		allow_bid = False
		context = {
			'asset' : asset,
			'now' : now,
			'allow_bid' : allow_bid,
			'end' : end,
		}
		return render(request, 'bidding/asset.html', context)

	if request.method == 'POST':
		if request.POST.get('delete'):
			# To Delete Asset
			try:
				Asset.objects.filter(id=id).delete()
				context = { 'success' : 'success'}
				return render(request, 'bidding/delete.html', context)
			except:
				context = { 'failed' : 'failed'}
				return render(request, 'bidding/delete.html', context)
		if request.POST.get('edit'):
			# To Edit Asset
			asset = get_object_or_404(Asset, id=id)
			context = {
				'asset' : asset,
				}
			return render(request, 'bidding/edit_asset.html', context)
		if request.POST.get('place_bid'):
			# To Place bid
			user_type = 'buyer'
			user_id = request.POST.get('user_id')
			bid_value = request.POST.get('bid_value')
			asset_id = request.POST.get('asset_id')
			try:
				# If buyer has already placed bid, update value	
				live_auction = get_object_or_404(LiveAuction, asset=asset_id, buyer=user_id)
				asset = get_object_or_404(Asset, id=id)
				live_auction_status = LiveAuction.objects.filter(Q(asset=asset_id)).order_by('price')
				if int(live_auction.price) < int(bid_value):
					# If bid value is greater than before 
					live_auction.price = bid_value
					live_auction.save()
					print("Value Updated")
					print("Bid Placed")
					context = {
						'asset' : asset,
						'now' : now,
						'allow_bid' : allow_bid,
						'placed' : 'placed',
						'about_to_end' : about_to_end,
						'live_auction_status' : live_auction_status
					}
					return render(request, 'bidding/asset.html', context)				
				else:
					# If bid value is less than before 
					print('Bid value must be greater than previous bid')
					context = {
						'asset' : asset,
						'now' : now,
						'allow_bid' : allow_bid,
						'min_value_error' : 'min_value_error',
						'about_to_end' : about_to_end,
						'live_auction_status' : live_auction_status
					}
					return render(request, 'bidding/asset.html', context)				

			except LiveAuction.DoesNotExist as e:
				asset_instance = get_object_or_404(Asset, id=asset_id)
				buyer_instance = get_object_or_404(Buyer, id=user_id)
				live_auction = LiveAuction.objects.create(
					asset=asset_instance,
					buyer=buyer_instance,
					price=bid_value,
				)
				live_auction.save()
				print('New Bid Value Placed')
				live_auction_status = LiveAuction.objects.filter(Q(asset=asset_id)).order_by('price')
				context = {
					'asset' : asset,
					'now' : now,
					'allow_bid' : allow_bid,
					'about_to_end' : about_to_end,
					'live_auction_status' : live_auction_status
				}
				return render(request, 'bidding/asset.html', context)
	try:
		asset = get_object_or_404(Asset, id=id)
		live_auction_status = LiveAuction.objects.filter(Q(asset=id)).order_by('price')
		
		# allow_bid = True # Temporary
		context = {
			'asset' : asset,
			'now' : now,
			'allow_bid' : allow_bid,
			'about_to_end' : about_to_end,
			'live_auction_status' : live_auction_status
		}
		return render(request, 'bidding/asset.html', context)
	except Exception as error:
		print(error)
		return HttpResponse(error)
		# return HttpResponse('<h1 style="text-align:center;">Asset Not Found</h1>')


def change_password(request):
	if request.method == 'POST':
		user_type = request.POST.get('user_type')
		user_id = request.POST.get('user_id')
		pwd1 = request.POST.get('pwd1')
		if user_type == 'seller':
			user = get_object_or_404(Seller, id=user_id)
		elif user_type == 'buyer':
			user = get_object_or_404(Buyer, id=user_id)
		else:
			return HttpResponse('Not Found')
		
		old_password = request.POST.get('old')

		if old_password == user.password:
			user.password = pwd1
			user.save()
			context = {
				'user' : user,
			}
			messages.success(request, 'Password Updated')
			return render(request, 'bidding/change_password.html', context)
		else:
			messages.error(request, 'Old Password is incorrect')
			context = {
				'user' : user,
			}
			return render(request, 'bidding/change_password.html', context)

		return render(request, 'bidding/{user_type}_dashboard.html', context)


def reset_password(request):
	if request.method == 'POST':
		global otp
		if request.POST.get('verify_otp'):
			# If otp matches, allow to reset password
			provided_otp = request.POST.get('otp')
			otp = 951
			if otp == provided_otp:
				return render(request, 'bidding/reset_password.html')
			else:
				context = {
					'verification_failed' : 'verification_failed'
				}
				return render(request, 'bidding/forgot_password.html', context)

		if request.POST.get('otp'):

			otp = random.randrange(10000000, 99999999)
			
			recepient = request.POST.get('forgot_email')
			print(recepient)
			subject = "One Time Password to reset your Password"
			message = "<h2>Your OTP to reset the password is </h2><h1>{0}</h1>".format(otp)
			send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = False)

			context = {
				'check_otp' : 'check_otp',
				'user_type' : request.POST.get('user_type')
			}
			return render(request, 'bidding/forgot_password.html', context)
		

		if request.POST.get('reset'):
			user_type = request.POST.get('user_type')
			user_id = request.POST.get('id')
			pwd1 = request.POST.get('pwd1')
			if user_type == 'seller':
				user = get_object_or_404(Seller, id=user_id)
			elif user_type == 'buyer':
				user = get_object_or_404(Buyer, id=user_id)
			else:
				return HttpResponse('Not Found')
			user.password = pwd1
			user.save()
			context = {
				'user' : user,
			}
			return render(request, 'bidding/{user_type}_dashboard.html', context)


# About
def about(request):
	return render(request, 'bidding/about.html')

# Logout
def logout(request):
	for key in list(request.session.keys()):
		del request.session[key]
	messages.success(request, "User Logged Out Successfully")
	return render(request, 'bidding/login.html')