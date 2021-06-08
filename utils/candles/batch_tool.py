from exchange.models import Fifteen_min_candle, Four_hour_candle, One_day_candle, One_hour_candle, One_min_candle, Five_min_candle, Market, One_week_candle, Currency
import requests, time, sys


candles_class = {
    '1min': One_min_candle,
    '5min': Five_min_candle,
    '15min': Fifteen_min_candle,
    '1hour': One_hour_candle,
    '4hour': Four_hour_candle,
    '1day': One_day_candle,
    '1week': One_week_candle
}

priods = {
    '1min': 60,
    '5min': 300,
    '15min': 900,
    '1hour': 3600,
    '4hour': 14400,
    '1day': 86400,
    '1week': 604800
}


# get a batch of source candles (eg. One_min_candle) and create one target candle (eg. Five_min_candle)
def batch_candles(candles_batch, open_time, market, target_class):
    target_class(
        market = market,
        open_time = open_time,
        open_price = candles_batch[0].open_price,
        close_price = candles_batch[-1].close_price,
        high_price = max([c.high_price for c in candles_batch]),
        low_price = min([c.low_price for c in candles_batch]),
        volume = sum([c.volume for c in candles_batch])
    ).save()
    print(market.name, open_time)


# 
def create_target_candles(market, source_interval, target_interval):
    global requests, time, candles_class, priods, batch_candles
    source_class = candles_class[source_interval]
    target_class = candles_class[target_interval]
    period = priods[target_interval]
    try:
        last_candle_time = target_class.objects.filter(market=market).last().open_time
    except:
        # it's only for the first time
        candles = requests.get(f'https://api.coinex.com/v1/market/kline?market={market.name}&limit=2&type={target_interval}').json()
        candles = candles['data']
        for candle in candles:
            target_class(market=market,open_time=candle[0], open_price=candle[1], close_price=candle[2], high_price=candle[3], low_price=candle[4], volume=candle[5]).save()
        if len(candles) != 0:
            print(market.name, f'fetched first {target_interval} candles')
        return

    try:
        start_open_time = last_candle_time + period
        source_candles = source_class.objects.filter(market=market, open_time__gte=start_open_time).order_by('open_time')
        open_time = start_open_time
        candles_batch = []
        for candle in source_candles:
            if candle.open_time >= open_time+period:
                batch_candles(candles_batch, open_time, market, target_class)
                candles_batch = []
                open_time += period
            candles_batch.append(candle)
            
    except Exception as e:
        print('error',market.name, e)