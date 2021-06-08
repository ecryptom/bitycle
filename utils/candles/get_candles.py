from datetime import datetime
from exchange.models import One_min_candle, Market, Currency
import requests, json, threading, time, os
from django.db.models import Q
from utils.mysql_engine import execute_sql
import redis, time

print(f'###################  {datetime.now()}  #############################')

# check if another instance of this program is working
redis_db = redis.Redis()
if redis_db.get('is_candle_updater_active') == b'True':
    exit()
redis_db.set('is_candle_updater_active', 'True')
redis_db.set('candle_updater_time', time.time())


sql = 'insert into exchange_one_min_candle (market_id, open_time, open_price, close_price, high_price, low_price, volume) values '

def get_candle(market, lock):
    global requests, sql, datetime, One_min_candle, time
    # calcute number of candles must be received
    try:
        now = int(datetime.now().timestamp())
        last_time = One_min_candle.objects.filter(market=market).order_by('open_time').last().open_time
        number_of_candles = (now - last_time) // 60
    except Exception as e:
        print('erro_1:', e)
        number_of_candles = 10
        if 'Too many connections' in str(e):
            execute_sql('SET GLOBAL max_connections = 1000;')

    # get candles and insert as a sql command
    try:
        candles = requests.get(f'https://api.coinex.com/v1/market/kline?market={market.name}&limit={number_of_candles}&type=1min').json()
        candles = candles['data']
        market_id = market.id
        time.sleep(0.1)
    
        lock.acquire()

        for candle in candles[:300][:-1]:
            sql += f'({market_id}, {candle[0]}, {candle[1]},{candle[2]},{candle[3]},{candle[4]}, {candle[5]}),'
        lock.release()
        #print(market.name, len(candles))

    except Exception as e:
        print('erro_2:', market.name, e)
        lock.release()



##################  create threads to get candles  ###############
try:
    toman = Currency.objects.get(symbol='TOMAN')
    lock = threading.Lock()
    delay = int(os.getenv('CANDLE_DELAY'))

    markets = Market.objects.filter(~Q(quote_currency=toman))
    number_of_threads = (markets.count() // 50)
    threads_range = [(50*i, 50*(i+1)) for i in range(number_of_threads)]
    threads_range.append((50*number_of_threads, markets.count()))

    for r in threads_range:
        # create threads
        trheads = []
        for market in markets[r[0]: r[1]]:
            trheads.append(threading.Thread(target=get_candle, args=(market, lock)))

        # start threads
        for trhead in trheads:
            trhead.start()

        # join threads
        for trhead in trheads:
            trhead.join()

        time.sleep(delay)

except Exception as e:
    print('erro_3:', e)


##################  save in db  ###############
try:
    sql = sql[:-1] + ';'
    execute_sql(sql)
except Exception as e:
    print('erro_4:', e)


redis_db.set('is_candle_updater_active', 'False')

print('######################  finish  ############################')