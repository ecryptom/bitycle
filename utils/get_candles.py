from datetime import datetime
from exchange.models import One_min_candle, Market, Currency
import requests, json, threading, time, os
from django.db.models import Q
import mysql.connector
import redis

# check if another instance of this program is working
redis_db = redis.Redis()
if redis_db.get('is_candle_updater_active') == b'True':
    exit()
redis_db.set('is_candle_updater_active', 'True')


sql = 'insert into exchange_one_min_candle (market_id, open_time, open_price, close_price, high_price, low_price) values '

def get_candle(market, lock):
    global requests, sql, datetime, One_min_candle, time, os
    # calcute number of candles must be received
    try:
        now = int(datetime.now().timestamp())
        last_time = One_min_candle.objects.filter(market=market).last().open_time
        number_of_candles = (now - last_time) // 60
    except Exception as e:
        print('@@@', e)
        number_of_candles = 1

    # get candles and insert as a sql command
    try:
        candles = requests.get(f'https://api.coinex.com/v1/market/kline?market={market.name}&limit={number_of_candles}&type=1min').json()
        candles = candles['data']
        market_id = market.id
        time.sleep(0.1)
    
        lock.acquire()
        for candle in candles[:300]:
            sql += f'({market_id}, {candle[0]}, {candle[1]},{candle[2]},{candle[3]},{candle[4]}),'
        lock.release()
        #print(market.name, len(candles))

    except Exception as e:
        print(e)



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
    print(e)


##################  save in db  ###############
try:
    sql = sql[:-1] + ';'

    mydb = mysql.connector.connect(
          host=os.getenv('DATABASE_HOST'),
          port=os.getenv('DATABASE_PORT'),
          user=os.getenv('DATABASE_USER_NAME'),
          password=os.getenv('DATABASE_USER_PASSWORD'),
          database=os.getenv('DATABASE_NAME'),
        )
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()

except Exception as e:
    print(e)


redis_db.set('is_candle_updater_active', 'False')