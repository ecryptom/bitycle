from ta.trend import IchimokuIndicator as ichi
from exchange.models import One_min_candle as candle_1m
from exchange.models import Market 
import time
from datetime import datetime
import pandas as pd
# from utils.bot_bale.bot import bot
from strategies.models import Indicator
from ta.trend import adx
from ta.momentum import stochrsi,stochrsi_k,stochrsi_d
from ta.volatility import BollingerBands as Boll




# input= [{'name':'ichimoku', 'lines':{'base_line':['above', 'lower', 'equal']}, 'setup':{'window1':'int', 'window2':'int', 'window3':'int', 'fillna':'bool', 'visual':'bool'}}]
# response_for_indicator_of_strategy = {1500:{'strategy':254645, 'name':'ichimoku', 'interval':'5m', 'last_value':2565, 'status':True, 'line':{'name':'base_line','action':{'name':'crosover','value_type':'indicator','value':'indicator-id'}}, 'setup':{'window1':5, 'window2':5, 'window3':5, 'fillna':False, 'visual':True}}, 1501:{'strategy':254645,'last-values':[2565,3645]'name':'ichimoku','user':'safari','status':True,'id':15658 ,'line':{'name':'base_line','last-value':2562,'action':{'name':'crosover','type':'indicator','selected':'indicator-id'}}}}

# response_for_one_line = {'strategy':254645,'last-values':[2565,3645]'name':'ichimoku','status':True,'line':{'name':'base_line','last-value':2562,'action':{'name':'crosover','type':'indicator','selected':'indicator-id'}}, 'setup':{'window1':5, 'window2':5, 'window3':5, 'fillna':False, 'visual':True}}

# a=Indicator.objects.first()
# print(a)

# def ichimoku(candles,lines=[],market_name,ncandle_last=3,ncandle_now=1,tolerance=2,window1=9,window2=26,window3=52,fillna=False,visual=False):


def ichimoku(candles, indicator, pre_results):
# doc indicator >>>>>>>>  https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html?highlight=ichimoku#ta.trend.IchimokuIndicator
    
    #### set result
    result={}
    result['strategy']=indicator.strategy.id
    result['interval']=indicator.interval
    result['name']=indicator.name
    result['action']=indicator.action
    result['status']=False


    setup=indicator.get_setup()
    tolerance=0.15################  must be between 0 and 1  #################
    df=candles
    line=indicator.line
    action=indicator.action
    
    
    my_ichi=ichi(high=df['high_price'],low=df['low_price'],window1=setup['window1'],window2=setup['window2'],window3=setup['window3'],fillna=setup['fillna'],visual=setup['visual'])


    ######### calc amount for conditions
    print(indicator.value_type)
    if indicator.value_type =='candle':
        print(2)
        # print(df)
        # amount=df[indicator.value].iloc[-1]
    if indicator.value_type == 'indicator':
        amount=pre_results['last-value']
    if indicator.value_type == 'num':
        amount=indicator.value
    amount=int(amount)    
        



    if line=='base_line':
        base_line=my_ichi.ichimoku_base_line()
        if action=='crosover':
            if base_line.iloc[-2]<amount*(1-tolerance) and base_line.iloc[-1]>amount*(1+tolerance):
                result['last_value']=base_line.iloc[-1] 
                result['status']=True

        if action=='crosunder':
            if base_line.iloc[-1]<amount*(1-tolerance) and base_line.iloc[-2]>amount*(1+tolerance):
                result['last_value']=base_line[-1] 
                result['status']=True

        if action=='equal':
            if amount*(1+tolerance)>base_line.iloc[-1]>amount*(1-tolerance)  :

                result['last_value']=base_line.iloc[-1] 
                result['status']=True

    if line=='conversion_line':
        conversion_line=my_ichi.ichimoku_conversion_line()
        if action=='crosover':
            if conversion_line.iloc[-2]<amount*(1-tolerance) and conversion_line.iloc[-1]>amount*(1+tolerance):
                result['last_value']=conversion_line.iloc[-1] 
                result['status']=True

        if action=='crosunder':
            if conversion_line.iloc[-1]<amount*(1-tolerance) and conversion_line.iloc[-2]>amount*(1+tolerance):
                result['last_value']=conversion_line.iloc[-1] 
                result['status']=True

        if action=='equal':
            if amount*(1+tolerance)>conversion_line.iloc[-1]>amount*(1-tolerance)  :

                result['last_value']=conversion_line.iloc[-1] 
                result['status']=True

    if line=='a':
        a=my_ichi.ichimoku_a()
        if action=='crosover':
            if a.iloc[-2]<amount*(1-tolerance) and a.iloc[-1]>amount*(1+tolerance):
                result['last_value']=a.iloc[-1] 
                result['status']=True

        if action=='crosunder':
            if a.iloc[-1]<amount*(1-tolerance) and a.iloc[-2]>amount*(1+tolerance):
                result['last_value']=a.iloc[-1] 
                result['status']=True

        if action=='equal':
            if amount*(1+tolerance)>a.iloc[-1]>amount*(1-tolerance)  :

                result['last_value']=a[-1] 
                result['status']=True

    if line=='b':

        b=my_ichi.ichimoku_b()
        if action=='crosover':
            if b.iloc[-2]<amount*(1-tolerance) and b.iloc[-1]>amount*(1+tolerance):
                result['last_value']=b.iloc[-1] 
                result['status']=True

        if action=='crosunder':
            if b.iloc[-1]<amount*(1-tolerance) and b.iloc[-2]>amount*(1+tolerance):
                result['last_value']=b.iloc[-1] 
                result['status']=True

        if action=='equal':
            if amount*(1+tolerance)>b.iloc[-1]>amount*(1-tolerance)  :

                result['last_value']=b.iloc[-1] 
                result['status']=True

    print('(!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!)')
    return result

def ADX(candles,indicator):
    my_adx=adx(high=df['high_price'],low=df['low_price'],close=df['close_price'],window=setup['window'],fillna=setup['fillna'])

                  
def StochRSI(candles,indicator):
# doc indicator >>>>>>>>  https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html?highlight=rsi#ta.momentum.RSIIndicator.rsi

    my_stochrsi=stochrsi(close=df['close_price'],window=setup['window'],smooth1=setup['smooth1'],smooth2=setup['smooth2'],fillna=setup['fillna'])
    my_stochrsik=stochrsi_k(close=df['close_price'],window=setup['window'],smooth1=setup['smooth1'],smooth2=setup['smooth2'],fillna=setup['fillna'])
    my_stochrsid=stochrsi_d(close=df['close_price'],window=setup['window'],smooth1=setup['smooth1'],smooth2=setup['smooth2'],fillna=setup['fillna'])

def BOLL(candles,indicator):
    pass

# for arz in Market.objects.all():
#     candles=list(candle_1m.objects.filter(market=arz).values())
#     df = pd.DataFrame(candles)

#     ichimoku(df,arz.name)

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
            
# my_stochrsid=stochrsi_d(close=df['close_price'],window=14,smooth1=14,smooth2=14,fillna=False)
# my_adx=ADX(high=df['high_price'],low=df['low_price'],close=df['close_price'],window=14,fillna=False)
# my_boll=Boll(close=df['close_price'],window=20,window_dev=2,fillna=False)
# # print(base_line)
