from django.urls import path
from django.conf.urls import url, re_path
from . import consumers

websocket_urlpatterns = [
    # path(r'asset/<int:id>/', consumers.LiveAuctioningConsumer),
    url(r'^asset/(?P<id>[0-9]+)/$', consumers.LiveAuctioningConsumer),
]