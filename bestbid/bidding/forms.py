# from django.forms import Textarea
from django import forms
from .models import *


class AssetForm(forms.ModelForm):
	# details = models.CharField(widget=forms.Textarea)
	class Meta:
		CATEGORY = (
				('CAR', 'CAR'),
				('HOUSE', 'HOUSE')
				)
		model = Asset
		fields = ['name', 'baseprice', 'image', 'category', 'details']
		widgets = {
			'name': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'placeholder' : 'Enter Asset Name',
				}
			),
			'baseprice': forms.NumberInput(
				attrs = {
					'class' : 'form-control',
					'placeholder' : 'Enter Base Price',
				}
			),
			'image': forms.FileInput(
				attrs = {
					'class' : 'form-control',
				}
			),
			'details' : forms.TextInput(
				
				attrs = {
					'cols': 80,
					'rows': 20,
					'class' : 'form-control',
					'placeholder' : 'Enter Description of the Asset',
				},
			),
		}


class BuyerForm(forms.ModelForm):
	class Meta:
		model = Buyer
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'name',
					'placeholder' : 'Enter Name',
				}
			),
			'email': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'email',
					'placeholder' : 'Enter Email',
				}
			),
			'password': forms.PasswordInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'email',
					'placeholder' : 'Enter Password',
				}
			),
			'contact': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'contact',
					'placeholder' : 'Enter Contact Number',
				}
			),
		}


class SellerForm(forms.ModelForm):
	class Meta:
		model = Seller
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'name',
					'placeholder' : 'Enter Name',
				}
			),
			'email': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'email',
					'placeholder' : 'Enter Email',
				}
			),
			'password': forms.PasswordInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'email',
					'placeholder' : 'Enter Password',
				}
			),
			'contact': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'contact',
					'placeholder' : 'Enter Contact Number',
				}
			),
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


class EditProfileForm(forms.ModelForm):
	
	class Meta:
		model = Seller
		fields = ['name', 'email', 'contact']
		widgets = {
			'name': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'name',
					'value' : "{{ user.name }}",
				}
			),
			'email': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'email',
					'value' : "{{ user.email }}",
				}
			),
			'contact': forms.TextInput(
				attrs = {
					'class' : 'form-control',
					'name' : 'contact',
					'value' : "{{ user.contact }}",
				}
			),
		}