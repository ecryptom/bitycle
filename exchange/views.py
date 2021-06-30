from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse
from rest_framework.views import APIView
from accounts.models import *
from exchange.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.utils import timezone
import json


def validate_data(data, required_data):
    for key in required_data:
        if key not in data:
            return False
    return True



class market_orders(APIView):
    def get(self, req):
        data = req.GET
        # check data
        if not validate_data(data, ['market']):
            return HttpResponseBadRequest(f"required_data: {['market']}")
        # check market
        market = Market.objects.filter(name=data['market'])
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        # get and send related orders
        sell_orders = Order.objects.filter(active=True, market=market[0], Type='sell').order_by('price')
        sell_orders = OrderSerializer(sell_orders, many=True).data
        buy_orders = Order.objects.filter(active=True, market=market[0], Type='buy').order_by('-price')
        buy_orders = OrderSerializer(buy_orders, many=True).data
        return Response({'sell_orders':sell_orders, 'buy_orders':buy_orders})


class markets(APIView):
    def get(self, req):
        table = {}
        rank = {}
        markets = Market.objects.all()
        for market in markets:
            if market.base_currency.symbol not in table:
                table[market.base_currency.symbol] = []
                rank[market.base_currency.symbol] = market.base_currency.rank
            table[market.base_currency.symbol].append(market.quote_currency.symbol)
        # sort table
        sorted_items = sorted(table.items(), key=lambda item: rank[item[0]])
        sorted_table = {item[0]:item[1] for item in sorted_items}
        return Response(sorted_table)        


class send_order(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, req):
        data = req.POST
        # check data
        if not validate_data(data, ['market', 'type', 'price', 'amount']):
            return HttpResponseBadRequest(f"required_data: {['market', 'type', 'price', 'amount']}")
        # check market
        market = Market.objects.filter(name=data['market'])
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        market = market[0]
        # check order type
        if data['type'] != 'sell' and data['type'] != 'buy':
            return Response({'status':'failed', 'error':'invalid type'})
        # check order amount
        if float(data['amount']) <= 0:
            return Response({'status':'failed', 'error':'invalid amount'})
        # check wallet balance
        if data['type'] == 'sell':
            wallet = req.user.get_wallet(market.base_currency)
            required_amount = float(data['amount'])
        elif data['type'] == 'buy':
            wallet = req.user.get_wallet(market.quote_currency)
            required_amount = float(data['amount']) * float(data['price'])
        if wallet.non_blocked_balance() < required_amount:
            return Response({'status':'failed', 'error':'low inventory'})
        # create order
        order = Order.objects.create(
          Type = data['type'],
          user = req.user,
          market = market,
          price = float(data['price']),
          total_amount = float(data['amount']),
          base_currency = market.base_currency,
          quote_currency = market.quote_currency
        )
        order.save()
        Orders_queue(order=order).save()
        return Response({'status':'suceess'})
        

class market_currencies(APIView):
    def get(self, req):
        data = req.GET
        # check data
        if not validate_data(data, ['market']):
            return HttpResponseBadRequest(f"required_data: {['market']}")
        # check market
        market = Market.objects.filter(name=data['market'])
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        return Response({
            'base_currency':CurrencySerializer(market[0].base_currency).data,
            'quote_currency':CurrencySerializer(market[0].quote_currency).data
        })
        
class market_info(APIView):
    def get(self, req):
        data = req.GET
        # check data
        if not validate_data(data, ['market']):
            return HttpResponseBadRequest(f"required_data: {['market']}")
        # check market
        market = Market.objects.filter(name=data['market'])
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        return Response(market[0].get_info())
        

class market_transactions(APIView):
    def get(self, req):
        data = req.GET
        # check data
        if not validate_data(data, ['market']):
            return HttpResponseBadRequest(f"required_data: {['market']}")
        # check market
        market = Market.objects.filter(name=data['market'])
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        transactions = list(market[0].transaction_set.all())[-20:]
        transactions = TransactionSerializer(transactions, many=True)
        return Response(transactions.data)


class deactivate_order(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, req):
        data = req.POST
        # check data
        if not validate_data(data, ['order_id']):
            return HttpResponseBadRequest(f"required_data: {['order_id']}")
        # check order
        order = Order.objects.filter(id=data['order_id'])
        if not order:
            return Response({'status':'failed', 'error':'invalid order_id'})
        order[0].active = False
        order[0].save()
        return Response({'status':'suceess'})


class top_markets_info(APIView):
    def get(self, req):
        tops = ['BTC', 'ETH', 'ADA', 'BNB']
        data = []
        for cur in tops:
            currency = Currency.objects.get(symbol=cur)
            data.append({
                'name': f'{cur}/USDT',
                'price': currency.price,
                'daily_change': "%.2f" % currency.daily_price_change_pct
            })
        return Response(data)
