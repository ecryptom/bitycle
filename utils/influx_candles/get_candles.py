from influxdb import InfluxDBClient
from datetime import datetime
from exchange.models import Market, Currency
import requests, threading, time, os
from django.db.models import Q
from django.utils import timezone
import redis, time, pytz

print(f'###################  {datetime.now()}  #############################')

# check if another instance of this program is working
redis_db = redis.Redis()
influx_client = InfluxDBClient()
influx_client.switch_database('coinex')

if redis_db.get('is_candle_updater_active') == b'True':
    exit()
redis_db.set('is_candle_updater_active', 'True')
redis_db.set('candle_updater_time', time.time())

points = []

def get_candle(market, lock):
    global requests, datetime, time, points, influx_client, timezone, pytz
    # calcute number of candles must be received
    try:
        now = int(datetime.now().timestamp())
        last_time = list(influx_client.query(f'select last("open"), time from one_min_candle where "market"=\'{market.name}\'').get_points())[0]['time']
        last_time = int(timezone.datetime.strptime(last_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.timezone('UTC')).timestamp())
        number_of_candles = (now - last_time) // 60
    except Exception as e:
        print('erro_1:', e)
        return

    # get candles and insert as a sql command
    try:
        candles = requests.get(f'https://api.coinex.com/v1/market/kline?market={market.name}&limit={number_of_candles}&type=1min').json()
        candles = candles['data']
        market_name = market.name
        time.sleep(0.1)
    
        lock.acquire()

        for candle in candles[:300][:-1]:
            points.append({
                "measurement": "one_min_candle",
                "tags": {
                    "market": market_name,
                },
                "time": int(candle[0]) * 1000000000,
                "fields": {
                    "open": float(candle[1]),
                    "close": float(candle[2]),
                    "high": float(candle[3]),
                    "low": float(candle[4]),
                    "volume":float(candle[5])
                }
            })
        lock.release()
        # print(market.name, len(candles))

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
            trhead.join(10)

        time.sleep(delay)

except Exception as e:
    print('erro_3:', e)


##################  save in db  ###############
try:
    influx_client.write_points(points)
except Exception as e:
    print('erro_4:', e)


redis_db.set('is_candle_updater_active', 'False')

print('######################  finish  ############################')