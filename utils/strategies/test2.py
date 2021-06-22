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
# from  backtrader.talib import BBANDS

df = pd.read_sql_query('select open_time, open_price, high_price, low_price, close_price from exchange_one_hour_candle where market_id=172', con=mydb,index_col='open_time', parse_dates=['open_time'],coerce_float=False)
# print(df)
df2=df.rename(columns={ 'open_time':'Date','open_price':'open','high_price':'high','low_price':'low','close_price':'close'})
df2 = df2[:-3]



datapath = ('./utils/mydata.txt')
df = pd.read_csv(
        datapath,
        parse_dates=['Date'],
        index_col='Date',
    )


data = bt.feeds.PandasData(dataname=df2,name='data_first')
cerebro = bt.Cerebro(stdstats=False)
cerebro.adddata(data)

class Strat1_2BD_5BH(bt.Strategy):
    def __init__(self):
        self.dataclose= self.datas[0].close    # Keep a reference to the "close" line in the data[0] dataseries
        self.order = None # Property to keep track of pending orders.  There are no orders when the strategy is initialized.
        self.buyprice = None
        self.buycomm = None


    def log(self, txt, dt=None):
        # Logging function for the strategy.  'txt' is the statement and 'dt' can be used to specify a specific datetime
        dt = dt or self.datas[0].datetime.date(0)
        print('{0},{1}'.format(dt.isoformat(),txt))
    
    def notify_order(self, order):
        # print(order,'\n\n\n',order.__dict__,'\n\n\n\n\n')
        # 1. If order is submitted/accepted, do nothing 
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 2. If order is buy/sell executed, report price executed
        if order.status in [order.Completed]: 
            if order.isbuy():
                self.log('BUY EXECUTED, Price: {0:8.2f}, Cost: {1:8.2f}, Comm: {2:8.2f}'.format(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm))
                
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, {0:8.2f}, Cost: {1:8.2f}, Comm{2:8.2f}'.format(
                    order.executed.price, 
                    order.executed.value,
                    order.executed.comm))
            
            self.bar_executed = len(self) #when was trade executed
        # 3. If order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            
        self.order = None
    
    def notify_trade(self,trade):
        # print('ooooooooo')
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(
            trade.pnl, trade.pnlcomm))
    
    def next(self):
        global datetime
        # Log the closing prices of the series from the reference
        self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order: # check if order is pending, if so, then break out
            return
                
        # since there is no order pending, are we in the market?    
        if not self.position: # not in the market
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    print('notif',self.datas[0].datetime.date())
                    self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                    self.order = self.buy()           
        else: # in the market
            if len(self) >= (self.bar_executed+5):
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell()


indicators_class = {'BollingerBands':bt.indicators.BollingerBands, 'macd':bt.indicators.MACD}
action_class = {'crossup':bt.indicators.CrossOver, 'crossdown':bt.indicators.CrossOver}
action_funcs = {'crossup':lambda x:x==1, 'crossdown':lambda x:x==-1}

class MyStrategy(bt.Strategy):
    global bt, indicators_class, action_class, action_funcs, Strategy

    params = (('ind', ['sma','bollinger']), ('doji', True),)

    INDS = ['sma','macd','bollinger']
    # INDS = ['sma', 'ema', 'stoc', 'rsi', 'macd', 'bollinger', 'aroon',
    #         'ultimate', 'trix', 'kama', 'adxr', 'dema', 'ppo', 'tema',
    #         'roc', 'williamsr']

    def __init__(self):
        global bt, indicators_class, action_class, action_funcs, Strategy

        # self.sma = bt.indicators.SimpleMovingAverage(period=2)
        # if self.p.doji:
        #         bt.talib.CDLDOJI(self.data.open, self.data.high,
        #                      self.data.low, self.data.close)
        
        # print(self.bb2.__dict__)
        # print(self.bb2.line1.__dict__)
        # print(self.p.ind[1])

         # self.indicators = [bt.indicators.BollingerBands(self.data, period=25), ]
        # self.mycroses=[bt.indicators.CrossOver(self.data.close,36000), bt.indicators.CrossOver(self.data.close,36000)]
        # self.funcs = [lambda x:x==1, lambda x:x==-1]


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
        print(self.datas[0].datetime.date(0),self.data.close[0], self.indicators[2][0], self.indicators[3][0])
        # print(f'up:{self.funcs[0](self.mycroses[1][0])},  down:{self.funcs[1](self.mycroses[1][0])}')
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

