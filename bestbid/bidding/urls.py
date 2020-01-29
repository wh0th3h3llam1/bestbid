from django.contrib.auth import login
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'bidding', views.bidding, name='bidding'),
	url(r'^login/$', login, {'template_name' : 'bidding/login.html'}),
	url(r'registration', views.registration, name='registration'),
]


#if settings.DEBUG:
#	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
