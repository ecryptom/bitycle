from utils.candles.batch_tool import *
from django.db.models import Q
from datetime import datetime

print(f'###################  {datetime.now()}  #############################')

source_interval = '5min'
target_interval = '15min'

toman = Currency.objects.get(symbol='TOMAN')
markets = Market.objects.filter(~Q(quote_currency=toman))

for market in markets:
    create_target_candles(market, source_interval, target_interval)


print('######################  finish  ############################')