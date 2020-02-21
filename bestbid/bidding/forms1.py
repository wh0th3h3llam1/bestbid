from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class AssetForm(ModelForm):

	class Meta:
		model = Asset
		fields = '__all__'


class BuyerForm(ModelForm):

	class Meta:
		model = Buyer
		fields = '__all__'


class SellerForm(ModelForm):

	class Meta:
		model = Seller
		fields = '__all__'


class BuyerRegistrationForm(ModelForm):
	class Meta:
		model = Buyer
		fields = '__all__'


class SellerRegistrationForm(ModelForm):
	class Meta:
		model = Seller
		fields = '__all__'


class BuyerLoginForm(ModelForm):
	
	class Meta:
		model = Buyer
		fields = ['email', 'password']


class SellerLoginForm(ModelForm):
	
	class Meta:
		model = Seller
		fields = ['email', 'password']

