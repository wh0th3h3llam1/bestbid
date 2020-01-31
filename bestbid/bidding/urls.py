from django.contrib.auth import login
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'login/', views.login, name='login'),
	url(r'agency/', views.agency, name='agency'),
 	url(r'index/', views.index, name='index'),
	url(r'registration/', views.registration, name='registration'),

	# url(r'login', login, {'template_name' : 'bidding/login.html'}),
]


#if settings.DEBUG:
#	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
