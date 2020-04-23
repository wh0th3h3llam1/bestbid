from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Asset)
admin.site.register(Auction)
admin.site.register(AuctionedAsset)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(LiveAuction)
