from exchange.models import *
from strategies.models import *
from .indicators import *
from datetime import datetime
import pandas as pd








data_frames = {}
functions = {'ichimoku': ichimoku}

strategies = Strategy.objects.all()
for strategy in strategies:

    results={market.name:{} for market in Market.objects.all()}
    for market in strategy.markets.all():

        for indicator in strategy.indicator_set.all():

            candle_class = indicator.get_candle_class()
            # check if there is a same data_frame
            if data_frames.get((market.name, candle_class)):
                df = data_frames[(market.name, candle_class)]
            else:
                candles = candle_class.objects.filter(market=market)
                candles = candles[candles.count()-100:].values()
                df = pd.DataFrame(candles)
                data_frames[(market.name, candle_class)] = df

            func = functions[indicator.name]
            result = func(df, indicator, results[market.name])
            results[market.name][indicator.id] = result

    # create and send message if strategy status is True
    for market, market_result in results.items():
        status = [indicator_result['status'] for ID, indicator_result in market_result.items()]
        if all(status):
            msg = f'Strategy : {strategy.name} \n\n'
            for indicator_id, indicator_result in market_result.items():
                msg += f'  {indicator_result['name']}\t{indicator_result['interval']}\n'
                msg += f'    values: {indicator_result['last-values']}\n'
            msg += f'\ntime : {datetime.now()}'
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(msg)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
