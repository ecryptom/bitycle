from django.db.models import manager
from django.utils import tree
from django.utils.translation import activate
from rest_framework.views import APIView
from accounts.models import *
from exchange.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.utils import timezone

class market_orders(APIView):
    def get(self, req):
        market = Market.objects.filter(name=req.GET.get('market'))
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        orders = Order.objects.filter(market=market[0], active=True)
        orders = OrderSerializer(orders, many=True)
        return Response(orders.data)


class send_order(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, req):
        market = Market.objects.filter(name=req.POST.get('market'))
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        if req.POST.get('type') != 'sell' and req.POST.get('type') != 'buy':
            return Response({'status':'failed', 'error':'invalid type'})
        order = Order.objects.create(
          Type = req.POST.get('type'),
          user = req.user,
          market = market[0],
          price = float(req.POST['price']),
          total_amount = float(req.POST['total_amount'])
        )
        Orders_queue(order=order).save()
        return Response({'status':'suceess'})
        