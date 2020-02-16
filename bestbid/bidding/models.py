from django.db import models

# Create your models here.


class Buyer(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(primary_key=True)
	password = models.CharField(max_length=50)
	contact = models.DecimalField(max_digits=10, decimal_places=0, default=0)

	def __str__(self):
		return self.name


class Seller(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(primary_key=True)
	password = models.CharField(max_length=50)
	contact = models.DecimalField(max_digits=10, decimal_places=0, default=0)

	def __str__(self):
		return self.name


class Asset(models.Model):

	CATEGORY = (
				('CAR', 'CAR'),
				('HOUSE', 'HOUSE')
				)
	name = models.CharField(max_length=50)
	baseprice = models.FloatField()
	image = models.ImageField(upload_to='uploads/')
	category = models.CharField(max_length=5, choices=CATEGORY)
	details = models.CharField(max_length=100)
	seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.name


class Auction(models.Model):
	CATEGORY = (
				('CAR', 'CAR'),
				('HOUSE', 'HOUSE')
				)
	category = models.CharField(max_length=5, choices=CATEGORY)
	date = models.DateTimeField(auto_now_add=True)
	

class AuctionedAsset(models.Model):
	CATEGORY = (
				('CAR', 'CAR'),
				('HOUSE', 'HOUSE')
				)
	
	auction_id = models.ForeignKey(Auction, null=True, on_delete=models.SET_NULL)
	asset = models.ForeignKey(Asset, null=True, on_delete=models.SET_NULL)
	seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL)
	buyer = models.ForeignKey(Buyer, null=True, on_delete=models.SET_NULL)
	category = models.CharField(max_length=5, null=True, choices=CATEGORY, default=None)
	price = models.FloatField()

	def __str__(self):
		return self.asset.name
