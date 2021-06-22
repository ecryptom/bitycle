import os, django
os.chdir('/home/ubuntu/services/backs/ecryptom')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecryptom.settings')
django.setup()

from accounts.models import *
from exchange.models import *
from strategies.models import *
from utils.strategies.indicators import *
import pandas as pd
import datetime
import backtrader as bt
import backtrader.feeds as feed
import os
import pandas as pd
from utils.mysql_engine import mydb

# m = Market.objects.get(name='BTCUSDT')

# candle=One_min_candle.objects.filter(market=m)
# df=pd.DataFrame(candle.values())
# ind=Indicator.objects.first()


# ichi=ichimoku(df,ind,{})
# # u = User.objects.first()
# s = Strategy.objects.get()
# setup = "{'window1':5, 'window2':5, 'window3':5, 'fillna':False, 'visual':True}"
# ind = Indicator(name='ichimoku', strategy=s, interval='1m', setup=setup, line='base_line', value_type='num', value='254', action='equal')

# last_time=datetime.datetime.fromtimestamp(df[-1:]['open_time'])

df = pd.read_sql_query('select open_time, open_price, high_price, low_price, close_price from exchange_one_min_candle where market_id=172', con=mydb,index_col='open_time', parse_dates=['open_time'],coerce_float=False)
# print(df)
df2=df.rename(columns={ 'open_time':'Date','open_price':'open','high_price':'high','low_price':'low','close_price':'close'})
# print(df2)
# df['Date']=df['open_time']
# df['open']=df['open_time']
# df2['Date']=df['open_time']

# m = Market.objects.get(name='BTCUSDT')
# candle=One_min_candle.objects.filter(market=m).order_by('open_time')[46500:47300]
# df=pd.DataFrame(candle.values())
# for i in range(len(df['open_time'])):
#     df['open_time'][i]=datetime.datetime.fromtimestamp(df['open_time'][i]).date()
# a=''
# print(df['open_time'])
# for i in range(len(df)):
#     a+=str(df['open_time'][i])+','+str(df['open_price'][i])+','+str(df['high_price'][i])+','+str(df['low_price'][i])+','+str(df['close_price'][i])+'\n'
# # print(a)
class PandasData(feed.DataBase):
    params = (
        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', 'open_time'),

        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', 'open_price'),
        ('high', 'high_price'),
        ('low', 'low_price'),
        ('close', 'close_price'),
        ('volume', 0),
        ('openinterest', 0),
    )


datapath = ('./utils/mydata.txt')

    # Simulate the header row isn't there if noheaders requested
    # skiprows = 1 if args.noheaders else 0
    # header = None if args.noheaders else 0

df = pd.read_csv(
        datapath,
        # skiprows=skiprows,
        # header=header,
        # parse_dates=[0],
        parse_dates=['Date'],
        index_col='Date',
    )

# datapath = ('./utils/orcl-1995-2014.txt')
# data = bt.feeds.YahooFinanceCSVData(
#     dataname=datapath,
#     fromdate=datetime.datetime(2000,1,1),
#     todate = datetime.datetime(2000,12,31),
#     reverse=False)


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
            # print(self.bar_executed)
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
                    # print('notif',self.datas[0].datetime.date())
                    self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))
                    self.order = self.buy()           
        else: # in the market
            if len(self) >= (self.bar_executed+5):
                self.log('SELL CREATE, {0:8.2f}'.format(self.dataclose[0]))
                self.order = self.sell()


class Macd_safari(bt.Strategy):
    global bt
    '''
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:
      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)
     - Set a stop price x times the ATR value away from the close
     - If in the market:
       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    '''

    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 3.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )

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
                
                # self.buyprice = order.executed.price
                # self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, {0:8.2f}, Cost: {1:8.2f}, Comm{2:8.2f}'.format(
                    order.executed.price, 
                    order.executed.value,
                    order.executed.comm))
            
            # self.bar_executed = len(self) #when was trade executed
            # print(self.bar_executed)
        # 3. If order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            
        self.order = None
    
     


    def __init__(self):

        if self.p.doji:
            bt.talib.CDLDOJI(self.data.open, self.data.high,
                             self.data.low, self.data.close)

        if self.p.ind == 'sma':
            bt.talib.SMA(self.data.close, timeperiod=25, plotname='TA_SMA')
            bt.indicators.SMA(self.data, period=25)
        elif self.p.ind == 'ema':
            bt.talib.EMA(timeperiod=25, plotname='TA_SMA')
            bt.indicators.EMA(period=25)
        elif self.p.ind == 'stoc':
            bt.talib.STOCH(self.data.high, self.data.low, self.data.close,
                           fastk_period=14, slowk_period=3, slowd_period=3,
                           plotname='TA_STOCH')

            bt.indicators.Stochastic(self.data)

        elif self.p.ind == 'macd':
            bt.talib.MACD(self.data, plotname='TA_MACD')
            bt.indicators.MACD(self.data)
            bt.indicators.MACDHisto(self.data)
        elif self.p.ind == 'bollinger':
            bt.talib.BBANDS(self.data, timeperiod=25,
                            plotname='TA_BBANDS')
            bt.indicators.BollingerBands(self.data, period=25)

        elif self.p.ind == 'rsi':
            bt.talib.RSI(self.data, plotname='TA_RSI')
            bt.indicators.RSI(self.data)

        elif self.p.ind == 'aroon':
            bt.talib.AROON(self.data.high, self.data.low, plotname='TA_AROON')
            bt.indicators.AroonIndicator(self.data)

        elif self.p.ind == 'ultimate':
            bt.talib.ULTOSC(self.data.high, self.data.low, self.data.close,
                            plotname='TA_ULTOSC')
            bt.indicators.UltimateOscillator(self.data)

        elif self.p.ind == 'trix':
            bt.talib.TRIX(self.data, timeperiod=25,  plotname='TA_TRIX')
            bt.indicators.Trix(self.data, period=25)

        elif self.p.ind == 'adxr':
            bt.talib.ADXR(self.data.high, self.data.low, self.data.close,
                          plotname='TA_ADXR')
            bt.indicators.ADXR(self.data)

        elif self.p.ind == 'kama':
            bt.talib.KAMA(self.data, timeperiod=25, plotname='TA_KAMA')
            bt.indicators.KAMA(self.data, period=25)

        elif self.p.ind == 'dema':
            bt.talib.DEMA(self.data, timeperiod=25, plotname='TA_DEMA')
            bt.indicators.DEMA(self.data, period=25)

        elif self.p.ind == 'ppo':
            bt.talib.PPO(self.data, plotname='TA_PPO')
            bt.indicators.PPO(self.data, _movav=bt.indicators.SMA)

        elif self.p.ind == 'tema':
            bt.talib.TEMA(self.data, timeperiod=25, plotname='TA_TEMA')
            bt.indicators.TEMA(self.data, period=25)

        elif self.p.ind == 'roc':
            bt.talib.ROC(self.data, timeperiod=12, plotname='TA_ROC')
            bt.talib.ROCP(self.data, timeperiod=12, plotname='TA_ROCP')
            bt.talib.ROCR(self.data, timeperiod=12, plotname='TA_ROCR')
            bt.talib.ROCR100(self.data, timeperiod=12, plotname='TA_ROCR100')
            bt.indicators.ROC(self.data, period=12)
            bt.indicators.Momentum(self.data, period=12)
            bt.indicators.MomentumOscillator(self.data, period=12)

        elif self.p.ind == 'williamsr':
            bt.talib.WILLR(self.data.high, self.data.low, self.data.close,
                           plotname='TA_WILLR')
            bt.indicators.WilliamsR(self.data)
























        self.dataclose= self.datas[0].close    # Keep a reference to the "close" line in the data[0] dataseries

        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def log(self, txt, dt=None):
        # Logging function for the strategy.  'txt' is the statement and 'dt' can be used to specify a specific datetime
        dt = dt or self.datas[0].datetime.date(0)
        print('{0},{1}'.format(dt.isoformat(),txt))
    
    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.mcross[0] > 0.0 and self.smadir < 0.0:
                self.order = self.buy()
                self.log('BUY CREATE {0:8.2f}'.format(self.dataclose[0]))

                # self.log('BUY EXECUTED, Price: {0:8.2f}, Cost: {1:8.2f}, Comm: {2:8.2f}'.format(
                #     self.order.executed.price,
                #     self.order.executed.value,
                #     self.order.executed.comm))
                pdist = self.atr[0] * self.p.atrdist
                self.pstop = self.data.close[0] - pdist

        else:  # in the market
            pclose = self.data.close[0]
            pstop = self.pstop

            if pclose < pstop:
                # self.close()  # stop met - get out
                self.order=self.sell()
                # self.log('SELL EXECUTED, {0:8.2f}, Cost: {1:8.2f}, Comm{2:8.2f}'.format(
                #     self.order.executed.price, 
                #     self.order.executed.value,
                #     self.order.executed.comm))
            else:
                pdist = self.atr[0] * self.p.atrdist
                # Update only if greater than
                self.pstop = max(pstop, pclose - pdist)

     

cerebro.addstrategy(Macd_safari) # We add the strategy described in the `Strategy class` cell
cerebro.broker.setcash(100000.0) # We set an initial trading capital of $100,000
cerebro.broker.setcommission(commission=0.001) # We set broker comissions of 0.1%


print('Starting Portfolio Value: {0:8.2f}'.format(cerebro.broker.getvalue()))
cerebro.run()
print('Final Portfolio Value: {0:8.2f}'.format(cerebro.broker.getvalue()))

