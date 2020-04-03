from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path, re_path
from django.conf import settings
from . import views

urlpatterns = [

	url(r'^adminLogin/$', views.adminLogin, name='adminLogin'),
	url(r'^home/$', views.home, name='home'),
	url(r'^bid/$', views.bid, name='bid'),
	url(r'^search/$', views.search, name='search'),

	url(r'^login/$', views.login, name='login'),
	url(r'^buyer_login/$', views.buyer_login, name='buyer_login'),
	url(r'^seller_login/$', views.seller_login, name='seller_login'),

	url(r'^registration/$', views.registration, name='registration'),
	url(r'^buyer_reg/$', views.buyer_reg, name='buyer_reg'),
	url(r'^seller_reg/$', views.seller_reg, name='seller_reg'),

	url(r'^buyer_dashboard/$', views.buyer_dashboard, name='buyer_dashboard'),
	url(r'^seller_dashboard/$', views.seller_dashboard, name='seller_dashboard'),

	# url(r'^profile/$', views.profile, name='profile'),
	re_path(r'^profile/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),

	url(r'^logout/$', views.logoutUser, name='logout'),

	url(r'^upload/$', views.upload, name='upload'),

	url(r'^index/$', views.index, name='index'),

	path('asset/<int:id>/', views.asset, name='asset'),
	# url(r'^asset/(?P<id>)\d+/$', views.asset, name='asset'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
