from ta.trend import IchimokuIndicator as ichi
from exchange.models import One_min_candle as candle_1m
from exchange.models import Market 
import time,datetime
import pandas as pd
from utils.bot_bale.bot import bot






input= [{'name':'ichimoku', 'lines':{'base_line':['above', 'lower', 'equal']}, 'setup':{'window1':'int', 'window2':'int', 'window3':'int', 'fillna':'bool', 'visual':'bool'}}]

response = [{'name':'ichimoku', 'lines':{'base_line':'above'}, 'setup':{'window1':5, 'window2':5, 'window3':5, 'fillna':False, 'visual':True}}]
def ichimoku(candles,lines=[],market_name,ncandle_last=3,ncandle_now=1,tolerance=2,window1=9,window2=26,window3=52,fillna=False,visual=False):
# just ncandle_now=1 work now    & ncandle last must be  odd & tolerance is diactive now
# doc indicator >>>>>>>>  https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html?highlight=ichimoku#ta.trend.IchimokuIndicator
    my_ichi=ichi(high=df['high_price'],low=df['low_price'],window1=window1,window2=window2,window3=window3)
    base_line=my_ichi.ichimoku_base_line()
    up_num=0
    down_num=0
    state_last='None'

    for candle in df[-ncandle_last:-ncandle_now]:
        for price in [candle['open_price'],candle['high_price'],candle['low_price'],candle['close_price']]:
            if price>base_line:
                up_num+=1
                break
            if price<base_line:
                down_num+=1
                break


    candle=df[-1:]
    for price in [candle['open_price'],candle['high_price'],candle['low_price'],candle['close_price']]:
        if up_num>down_num:
            if price<base_line:
                signal='SELL'
                signal_status='🔴'
                # state_last=' in last market above of ichimoku'
                message=f'{signal_status}{market_name}\tsignal:{signal}\t name:ichimoku{window1}-{window2}-{window3}\ncandle-1m: o:{candle['open_price']} h:{candle['high_price']} c:{candle['close_price']} l:{candle['low_price']}\ntime:{time.time()}'
                send_msg(message)
                break
        
        else:
            if price>base_line:
                signal='BUY'
                signal_status='🟢'
                # state_last='in last market is under ichimoku'
                message=f'{signal_status}{market_name}\tsignal:{signal}\t name:ichimoku{window1}-{window2}-{window3}\ncandle-1m: o:{candle['open_price']} h:{candle['high_price']} c:{candle['close_price']} l:{candle['low_price']}\ntime:{time.time()}'
                send_msg(message)
                break


def boll_rsi()





for arz in Market.objects.all():
    candles=list(candle_1m.objects.filter(market=arz).values())
    df = pd.DataFrame(candles)

    ichimoku(df,arz.name)

# print(df[-1:])
# last_time=datetime.datetime.fromtimestamp(df[-1:]['open_time'])
# print(last_time)
# my_ichi=ichi(high=df['high_price'],low=df['low_price'],window1=103,window2=103,window3=103)
# base_line=my_ichi.ichimoku_base_line()
# up_num=0
# down_num=0
# for candle in df[-3:]:
#     for price in [candle['open_price'],candle['high_price'],candle['low_price'],candle['close_price']]:
#         if price>base_line:
#             up_num+=1
#             break
#         if price<base_line:
#             down_num+=1
#             break
            

# print(base_line)
