from exchange.models import One_min_candle, Market, Currency
from django.db.models import Q
import pandas as pd
import datetime, time, requests
from django.core.mail import send_mail
from django.conf import settings

print(f'###################  {datetime.datetime.now()}  #############################')

# get tow timestamp and check candles between them in the related market
# return timestamps that we hava no candle
def check(market, start, end=time.time()):
    global One_min_candle, time, pd, Market
    if type(market) == str:
        market = Market.objects.get(name=market)
    candles = One_min_candle.objects.filter(market=market, open_time__lte=end, open_time__gte=start).order_by('open_time')
    df = pd.DataFrame(candles.values())
    times = df['open_time']
    gap_times = []
    for i in range(1, len(times)):
        dif = times[i] - times[i-1]
        if dif < 0:
            print('negetive!!')
        if dif == 0:
            print('duplicat candle',market.name,times[i])
        elif dif != 60:
            for t in range(times[i-1]+60, times[i], 60):
                gap_times.append(t)
    return gap_times
    

# get gap_times and fetch them from coinex
def fill_gaps(market, gaps):
    global One_min_candle, time, Market, requests
    if type(market) == str:
        market = Market.objects.get(name=market)

    now = int(time.time())
    number_of_candles = (now - min(gaps)) // 60

    candles = requests.get(f'https://api.coinex.com/v1/market/kline?market={market.name}&limit={number_of_candles+1}&type=1min').json()
    candles = candles['data']
    time.sleep(0.1)


    for candle in candles:
        if candle[0] in gaps:
            One_min_candle(
                market=market,
                open_time = candle[0],
                open_price = candle[1],
                close_price = candle[2],
                high_price = candle[3],
                low_price = candle[4],
            ).save()

    
    

msg = ''
toman = Currency.objects.get(symbol='TOMAN')
markets = Market.objects.filter(~Q(quote_currency=toman))
for market in markets:
    try:
        start = time.time() - 3600*17
        gaps = check(market, start)
        if gaps:
            msg += f'market {market.name} had {len(gaps)} gaps, '
            fill_gaps(market, gaps)
            gaps = check(market, start)
            msg += f'now has {len(gaps)} \n'
    except Exception as e:
        print('error', market.name, e)

if not msg:
    msg = 'congratulation, there was not any gaps in our candles!'

# notif
if msg: 
    send_mail(
        subject='gaps in candles',
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['mr.mirshamsi.78@gmail.com', 'mojtabasafari19@gmail.com '],
    )

print('######################  finish  ############################')