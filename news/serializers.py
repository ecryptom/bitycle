from rest_framework import serializers
from .models import *

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'body', 'date', 'src_name', 'src_link', 'pump', 'dump']