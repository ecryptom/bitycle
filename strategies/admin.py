from django.contrib import admin
from .models import *


admin.site.register(Strategy)

@admin.register(Indicator)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name','strategy','interval','action','value_type')

@admin.register(Candle_pattern)
class MyModelAdmin2(admin.ModelAdmin):
    list_display = ('name_en', 'kind', 'interval')