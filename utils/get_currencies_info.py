import requests, json
from datetime import datetime
from exchange.models import Currency
from multiprocessing import Process
from django.db.models import Q

print(f'###################  {datetime.now()}  #############################')

def update(currencies):
    global json, requests, Currency
    symbols = [c.symbol for c in currencies]
    symbols = ','.join(symbols)
    response = requests.get(f'https://api.nomics.com/v1/currencies/ticker?key=e46fab48a3538b1ec642482aaa54fb68&ids={symbols}&interval=1d,7d')
    currencies_info = json.loads(response.content.decode().replace('\n', ''))
    for cur_info in currencies_info:
        try:
            cur = Currency.objects.get(symbol=cur_info['id'])
            cur.price = cur_info['price']
            try:
                cur.market_cap = cur_info['market_cap']
            except:
                pass
            try:
                cur.daily_price_change_pct = float(cur_info['1d']['price_change_pct'])*100
            except:
                pass
            try:
                cur.weekly_price_change_pct = float(cur_info['7d']['price_change_pct'])*100
            except:
                pass
            try:
                cur.turnover = cur_info['1d']['volume']
            except:
                pass
            cur.save()
        except Exception as e:
            print('error1:', e)

def update_with_limit(currencies, t):
    global Process, update
    p = Process(target=update, args=(currencies, ))
    p.start()
    p.join(t)
    if p.is_alive():
        p.terminate()

all_currencies = Currency.objects.filter(~Q(name='TOMAN'))

update_with_limit(all_currencies, 40)

print('######################  finish  ############################')