from django.contrib import admin
from exchange.models import *

admin.site.register(Currency)
admin.site.register(Transaction)
# admin.site.register(Market)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user','currency','balance')
    ordering = ['id']
    search_fields = ('currency','id')

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name']
    search_fields = ('name',)

@admin.register(Order)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('user', 'market', 'total_amount', 'price', 'active', 'market')
    search_fields = ('user',)
