from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class AssetForm(forms.ModelForm):

	class Meta:
		model = Asset
		fields = '__all__'


class BuyerForm(forms.ModelForm):

	class Meta:
		model = Buyer
		fields = '__all__'
		widgets = {
			'password': forms.PasswordInput()
		}


class SellerForm(forms.ModelForm):

	class Meta:
		model = Seller
		fields = '__all__'
		widgets = {
			'password': forms.PasswordInput()
		}

class BuyerRegistrationForm(forms.ModelForm):
	class Meta:
		model = Buyer
		fields = '__all__'
		widgets = {
			'password': forms.PasswordInput()
		}


class SellerRegistrationForm(forms.ModelForm):
	class Meta:
		model = Seller
		fields = '__all__'
		widgets = {
			'password': forms.PasswordInput()
		}

class BuyerLoginForm(forms.ModelForm):
	
	class Meta:
		model = Buyer
		fields = ['email', 'password']
		widgets = {
			'email': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'placeholder' : 'Enter Email',
				}
			),
			'password': forms.PasswordInput(
				attrs = {
					'placeholder' : 'Enter Password',
					'class' : 'form-control'
				}
			),
		}

class SellerLoginForm(forms.ModelForm):
	
	class Meta:
		model = Seller
		fields = ['email', 'password']
		widgets = {
			'email': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'placeholder' : 'Enter Email',
				}
			),
			'password': forms.PasswordInput(
				attrs = {
					'placeholder' : 'Enter Password',
					'class' : 'form-control'
				}
			),
		}
