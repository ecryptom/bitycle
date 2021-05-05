from datetime import datetime
from exchange.models import *
import requests, json

five_min_ago = datetime.now().timestamp() - 310

symbols = [(cur.symbol, cur.id) for cur in Currency.objects.all()[:5]]

sql = '''INSERT INTO 
    exchange_five_min_candle(currency_id, open_time, close_time, open_price, close_price, number_of_trades, high_price, low_price, volume)
    VALUES'''
for symbol, cur_id in symbols:
    try:
        candles = requests.get('https://api.binance.com/api/v3/klines', params={
            'symbol': f'{symbol}USDT',
            'interval': '5m',
            'startTime': int(five_min_ago) * 1000
        })
        last_candle = json.loads(candles.content)[-1]
        sql += f'''
        ({cur_id}, {last_candle[0]/1000}, {last_candle[6]/1000}, {float(last_candle[1])}, {float(last_candle[4])}, {int(last_candle[8])}, {float(last_candle[2])}, {float(last_candle[3])}, {float(last_candle[5])}),'''
    except Exception as e:
        print('!!!!!!!!!!!!!!', symbol)
        print(e)

sql = sql[:-1] + ';'
print(sql)

