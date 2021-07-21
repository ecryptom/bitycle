from influxdb import InfluxDBClient
from datetime import datetime
from exchange.models import Market, Currency
from django.db.models import Q
from django.utils import timezone
import pytz


print(f'###################  {datetime.now()}  #############################')

influx_client = InfluxDBClient()
influx_client.switch_database('coinex')

toman = Currency.objects.get(symbol='TOMAN')
markets = Market.objects.filter(~Q(quote_currency=toman))

source_interval = 'fifteen_min_candle'
destination_interval = 'one_hour_candle'
group_by = '1h'

for market in markets:
    try:
        last_time = list(influx_client.query(f'select last("open"), time from {destination_interval} where "market"=\'{market.name}\'').get_points())[0]['time']
        last_time = int(timezone.datetime.strptime(last_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.timezone('UTC')).timestamp())

        q = f'SELECT first(open) AS open, last(close) AS close,max(high) AS high,min(low) AS low,sum(volume) AS volume into {destination_interval} FROM {source_interval} WHERE market=\'{market.name}\' and time >= {last_time}s GROUP BY time({group_by}), market'
        p = influx_client.query(q)
        # print(p)
        # print(market.name)
    except Exception as e:
        print('!!!', market.name, e)

print('######################  finish  ############################')