from django import forms


class Assets(forms.Form):

	a_name = forms.CharField(label="Asset Name", max_length=50)
	a_baseprice = forms.DecimalField(label="Enter Base Price", max_length=10)
	a_img = forms.ImageField(label="Upload An Image")
	a_type = forms.CharField(label="Asset Type", max_length=2)
	a_details = forms.CharField(label="Asset Name", max_length=100)


class Buyer(forms.Form):

	b_name = forms.CharField(label="Asset Name", max_length=50)
	email = forms.EmailField(label="Enter Email")
	password = forms.
	b_contact = forms.


class Seller(forms.Form):

	a_name = forms.CharField(label="Seller Name", max_length=50)
	email = forms.EmailField()
	password = forms.
	s_contact = forms.
