from rest_framework import serializers
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'Type', 'price', 'market', 'remaining_amount', ]