from rest_framework import serializers
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'Type', 'price', 'market_name', 'remaining_amount', 'date']

class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'Type', 'price', 'market_name', 'total_amount', 'traded_amount', 'total_price', 'average_traded_price', 'date']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name', 'symbol', 'persian_name', 'logo']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['price', 'amount', 'date']