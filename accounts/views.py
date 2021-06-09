from rest_framework import response
from django.http import HttpResponseBadRequest
from accounts.models import User
from exchange.models import *
from exchange.serializers import UserOrderSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import re, random, time
from django.utils import timezone

def validate_data(data, required_data):
    for key in required_data:
        if key not in data:
            return False
    return True


class register(APIView):
    def post(self, req):
        data = req.POST
        # check data
        if not validate_data(data, ['username', 'password', 'phone']):
            return HttpResponseBadRequest(f"required_data: {['username', 'password', 'phone']}")
        #check username if it's not available or not verified before
        user = User.objects.filter(username=req.POST.get('username'))
        if user:
            return Response({'status':'failed', 'error':'not available username'})
        #create a new user
        invite_code = int(time.time())
        user = User.objects.create(username=data['username'], email='bitycle@gmail.com', name='ali', password=data['password'], phone=data['phone'], invite_code=invite_code)
        token, status = Token.objects.get_or_create(user=user)
        return Response({'status':'success', 'token':f'Token {token.key}'})

    

class login(APIView):
    def post(self, req):
        data = req.POST
        # check data
        if not validate_data(data, ['username', 'password']):
            return HttpResponseBadRequest(f"required_data: {['username', 'password']}")
        user = User.objects.filter(username=data['username'])
        if user and user[0].check_password(data['password']):
            auth.login(req, user[0])
            token, status = Token.objects.get_or_create(user=user[0])
            return Response({'status':'success', 'token':f'Token {token.key}'})
        return Response({'status':'failed', 'error':'not found'})



class user_market_orders(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, req):
        data = req.GET
        # check data
        if not validate_data(data, ['market']):
            return HttpResponseBadRequest(f"required_data: {['market']}")
        # check market
        market = Market.objects.filter(name=data['market'])
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        orders = req.user.order_set.filter(market=market[0]).order_by('-id')
        orders = UserOrderSerializer(orders, many=True)
        return Response(orders.data)


class user_active_market_orders(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, req):
        data = req.GET
        # check data
        if not validate_data(data, ['market']):
            return HttpResponseBadRequest(f"required_data: {['market']}")
        # check market
        market = Market.objects.filter(name=data['market'])
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        orders = req.user.order_set.filter(active=True, market=market[0]).order_by('-id')
        orders = UserOrderSerializer(orders, many=True)
        return Response(orders.data)