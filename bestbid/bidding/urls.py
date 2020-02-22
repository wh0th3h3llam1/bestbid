from django.conf.urls.static import static
from django.contrib.auth import login
from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
	
	url(r'^adminLogin/$', views.adminLogin, name='adminLogin'),
	url(r'^home/$', views.home, name='home'),
	
	url(r'^login/$', views.login, name='login'),
	url(r'^buyer_login/$', views.buyer_login, name='buyer_login'),
	url(r'^seller_login/$', views.seller_login, name='seller_login'),

	url(r'^registration/$', views.registration, name='registration'),
	url(r'^buyer_reg/$', views.buyer_reg, name='buyer_reg'),
	url(r'^seller_reg/$', views.seller_reg, name='seller_reg'),

	url(r'^buyer_dashboard/$', views.buyer_dashboard, name='buyer_dashboard'),
	url(r'^seller_dashboard/$', views.seller_dashboard, name='seller_dashboard'),

	url(r'^profile/$', views.profile, name='profile'),

	url(r'^logout/$', views.logoutUser, name='logout'),

	url(r'^search/$', views.search, name='search'),

	url(r'^index/$', views.index, name='index'),

	# url(r'^login$', login, {'template_name' : 'bidding/login.html'}),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
