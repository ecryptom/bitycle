from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from accounts.models import *
from exchange.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.utils import timezone


def validate_data(data, required_data):
    for key in required_data:
        if key not in data:
            return False
    return True


class market_news(APIView):
    def get(self, req):
        data = req.GET
        # check data
        if not validate_data(data, ['market']):
            return HttpResponseBadRequest(f"required_data: {['market']}")
        # check market
        market = Market.objects.filter(name=data['market'])
        if not market:
            return Response({'status':'failed', 'error':'invalid market'})
        news = list(market[0].base_currency.news_set.all())[:10]
        news.extend(list(market[0].quote_currency.news_set.all())[:10])
        news = NewsSerializer(news, many=True)
        return Response(news.data)

