from django.contrib import admin
from news.models import News


@admin.register(News)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('title','date','related','post_id_arzdg','src_name','dump','pump')
    search_fields = ['title']
    ordering = ['-post_id_arzdg']