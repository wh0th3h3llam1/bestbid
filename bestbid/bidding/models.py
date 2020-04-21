from django.urls import reverse
from django.db import models

# Create your models here.


class Buyer(models.Model):
	name = models.CharField(max_length=50, blank=False)
	email = models.EmailField(unique=True, blank=False)
	password = models.CharField(max_length=50, blank=False)
	contact = models.DecimalField(max_digits=10, decimal_places=0, default=0, blank=False)

	def __str__(self):
		return self.name

	def get_abs_url(self):
		return reverse("buyer", kwargs={"id" : self.id})
		# return f"/buyer/{self.id}"


class Seller(models.Model):
	name = models.CharField(max_length=50, blank=False)
	email = models.EmailField(unique=True, blank=False)
	password = models.CharField(max_length=50, blank=False)
	contact = models.DecimalField(max_digits=10, decimal_places=0, default=0, blank=False)

	def __str__(self):
		return self.name

	def get_abs_url(self):
		return reverse("seller", kwargs={"id" : self.id})
		# return f"/seller/{self.id}"


class Asset(models.Model):

	CATEGORY = (
				('CAR', 'CAR'),
				('HOUSE', 'HOUSE')
				)
	name = models.CharField(max_length=50, blank=False)
	baseprice = models.DecimalField(max_digits=9, decimal_places=0, blank=False)
	image = models.ImageField(upload_to='uploads/', blank=False)
	category = models.CharField(max_length=5, choices=CATEGORY, blank=False)
	details = models.CharField(max_length=100, blank=False)
	seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL, blank=False)
	sold = models.BooleanField(default=False)
	
	def __str__(self):
		return self.name

	def get_abs_url(self):
		return reverse("asset", kwargs={"id" : self.id})
		# return f"/asset/{self.id}"


class Auction(models.Model):
	CATEGORY = (
				('CAR', 'CAR'),
				('HOUSE', 'HOUSE')
				)
	category = models.CharField(max_length=5, choices=CATEGORY)
	date = models.DateTimeField(auto_now_add=True, blank=False)

	def __str__(self):
		return str(self.id)


'''
class LiveAuction(models.Model):
	asset_id = 
	buyer_id = 
	price = 
	date_time = 
'''


class AuctionedAsset(models.Model):
	CATEGORY = (
				('CAR', 'CAR'),
				('HOUSE', 'HOUSE')
				)
	
	auction_id = models.ForeignKey(Auction, null=True, on_delete=models.CASCADE)
	asset = models.ForeignKey(Asset, null=True, on_delete=models.CASCADE)
	seller = models.ForeignKey(Seller, null=True, on_delete=models.CASCADE)
	buyer = models.ForeignKey(Buyer, null=True, on_delete=models.CASCADE)
	category = models.CharField(max_length=5, null=True, choices=CATEGORY, default=None)
	price = models.DecimalField(max_digits=9, decimal_places=0, blank=False)

	def __str__(self):
		return self.asset.name