from exchange.models import *

all_candles = One_min_candle.objects.all()
m = Market.objects.get(name="BTCUSDT")
btc_candles = One_min_candle.objects.filter(market=m)
l = range(4000000, all_candles.count())
for i in l:
    dif = (all_candles[i].open_time - all_candles[i-1].open_time) / 60
    print(1, end='\t')

import time
from exchange.models import *

all_candles = One_min_candle.objects.all()
m = Market.objects.get(name="BTCUSDT")
btc_candles = One_min_candle.objects.filter(market=m)

a = time.time()
l = [c.id for c in all_candles]
b = time.time()
print(b-a)