from datetime import datetime
from exchange.models import Currency, Five_min_candle
import requests, json

five_min_ago = datetime.now().timestamp() - 310

a = Currency.objects.all()
i=1
for cur in a:
    try:
        candles = requests.get('https://api.binance.com/api/v3/klines', params={
            'symbol': f'{cur.symbol}USDT',
            'interval': '5m',
            'startTime': int(five_min_ago) * 1000
        })
        last_candle = json.loads(candles.content)[-1]
        Five_min_candle(
            currency = cur,
            open_time = last_candle[0]/1000,
            close_time = last_candle[6]/1000,
            open_price = float(last_candle[1]),
            close_price = float(last_candle[4]),
            number_of_trades = int(last_candle[8]),
            high_price = float(last_candle[2]),
            low_price = float(last_candle[3]),
            volume = float(last_candle[5])
        ).save()
        i+=1
    except Exception as e:
        print('!!!!!!!!!!!!!!', cur.name)
        print(e)
        #if cur.name != 'tether':
        #    cur.delete()

