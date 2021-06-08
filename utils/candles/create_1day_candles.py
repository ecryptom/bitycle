from utils.candles.batch_tool import *
from django.db.models import Q
from datetime import datetime
import redis, time

print(f'###################  {datetime.now()}  #############################')

# check if another instance of this program is working
redis_db = redis.Redis()
if redis_db.get('is_1day_candle_creator_active') == b'True':
    exit()
redis_db.set('is_1day_candle_creator_active', 'True')
redis_db.set('1day_candle_creator_time', time.time())



source_interval = '4hour'
target_interval = '1day'

toman = Currency.objects.get(symbol='TOMAN')
markets = Market.objects.filter(~Q(quote_currency=toman))

for market in markets:
    create_target_candles(market, source_interval, target_interval)



redis_db.set('is_1day_candle_creator_active', 'False')

print('######################  finish  ############################')