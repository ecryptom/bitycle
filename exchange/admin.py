from django.contrib import admin
from exchange.models import *

admin.site.register(Currency)
admin.site.register(Transaction)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user','currency','balance')
    ordering = ['id']

