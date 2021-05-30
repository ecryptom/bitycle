
from accounts.models import *
from exchange.models import *
from strategies.models import *
from utils.strategies.indicators import *
import pandas as pd
import datetime
m = Market.objects.get(name='BTCUSDT')

candle=One_min_candle.objects.filter(market=m)
df=pd.DataFrame(candle.values())
ind=Indicator.objects.first()


ichi=ichimoku(df,ind,{})
# u = User.objects.first()
s = Strategy.objects.get()
setup = "{'window1':5, 'window2':5, 'window3':5, 'fillna':False, 'visual':True}"
ind = Indicator(name='ichimoku', strategy=s, interval='1m', setup=setup, line='base_line', value_type='num', value='254', action='equal')

last_time=datetime.datetime.fromtimestamp(df[-1:]['open_time'])
