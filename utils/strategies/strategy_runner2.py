from accounts.models import *
from exchange.models import *
from strategies.models import Strategy, Indicator
import pandas as pd
import datetime
import backtrader as bt
import backtrader.feeds as feed
import os
import pandas as pd
from utils.mysql_engine import mydb


df = pd.read_sql_query('select open_time, open_price, high_price, low_price, close_price from exchange_one_hour_candle where market_id=172', con=mydb,index_col='open_time', parse_dates=['open_time'],coerce_float=False)
df2=df.rename(columns={ 'open_time':'Date','open_price':'open','high_price':'high','low_price':'low','close_price':'close'})
df2 = df2[:-3]


data = bt.feeds.PandasData(dataname=df2,name='data_first')
cerebro = bt.Cerebro(stdstats=False)
cerebro.adddata(data)



indicators_class = {'BollingerBands':bt.indicators.BollingerBands, 'macd':bt.indicators.MACD}
action_class = {'crossup':bt.indicators.CrossOver, 'crossdown':bt.indicators.CrossOver}
action_funcs = {'crossup':lambda x:x==1, 'crossdown':lambda x:x==-1}


class MyStrategy(bt.Strategy):
    global bt, indicators_class, action_class, action_funcs, Strategy
    params = (('ind', ['sma','bollinger']), ('doji', True),)
    INDS = ['sma','macd','bollinger']

    def __init__(self):
        global bt, indicators_class, action_class, action_funcs, Strategy

        self.actions = []
        self.funcs = []
        self.indicators = {}

        s = Strategy.objects.first()
        indicators = s.indicator_set.all()
        
        for ind in indicators:
            indicator = indicators_class[f'{ind.name}'](self.data, **ind.get_setup())
            indicator = getattr(indicator, ind.line)
            self.indicators[ind.id] = indicator

            if ind.value_type == 'candle':
                line2 = getattr(self.data, ind.value)
            elif ind.value_type == 'num':
                line2 = int(ind.value)
            elif ind.value_type == 'indicator':
                line2 = self.indicators[int(ind.value)]
            
            self.actions.append(action_class[ind.action](indicator, line2))
            self.funcs.append(action_funcs[ind.action])

        self.length = len(self.actions)



    def next(self):
        # print(self.datas[0].datetime.date(0),self.data.close[0], self.indicators[2][0], self.indicators[3][0])
        l = []
        for i in range(self.length):
            l.append(self.funcs[i](self.actions[i][0]))
        print(l)


     

cerebro.addstrategy(MyStrategy) # We add the strategy described in the `Strategy class` cell
cerebro.broker.setcash(100000.0) # We set an initial trading capital of $100,000
cerebro.broker.setcommission(commission=0.001) # We set broker comissions of 0.1%


print('Starting Portfolio Value: {0:8.2f}'.format(cerebro.broker.getvalue()))
cerebro.run()
print('Final Portfolio Value: {0:8.2f}'.format(cerebro.broker.getvalue()))

