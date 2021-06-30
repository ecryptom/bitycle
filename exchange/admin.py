from django.contrib import admin
from exchange.models import *

admin.site.register(Currency)
admin.site.register(Wallet)
admin.site.register(Transaction)

