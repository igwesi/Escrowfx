from django.contrib import admin
# Register your models here.
from .models import Wallet, payoutLink

admin.site.register(Wallet)

@admin.register(payoutLink)
class PayoutLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'seller', 'buyer_currency', 'seller_currency', 'buyer_amount', 'seller_amount', 'status', 'date_created')
    list_display_links = ('id', 'buyer', 'seller', 'buyer_currency', 'seller_currency', 'buyer_amount', 'seller_amount', 'status', 'date_created')
    list_filter = ('status', 'date_created')
    search_fields = ('buyer', 'seller', 'buyer_currency', 'seller_currency', 'buyer_amount', 'seller_amount', 'status', 'date_created')