from exchange.models import One_min_candle, Currency, Order, Orders_queue, Market
from accounts.models import User
from django.utils import timezone
import random
from django.db.models import Q
from utils.mysql_engine import execute_sql
from datetime import datetime


print(f'###################  {datetime.now()}  #############################')

ecryptom_user = User.objects.get(username='ecryptom')
dollar = 25000

deactive_orders_sql = 'INSERT INTO exchange_order (id, Type, user_id, market_id, price, total_amount, traded_amount,date, expire_date, active) VALUES '
add_orders_sql = 'insert into exchange_order (Type, user_id, market_id, price, total_amount, traded_amount,date, expire_date, active) values '

def update_orders(market, price, Type, average_volume, number_of_orders):
    global Currency, Order, timezone, ecryptom_user, random, dollar, Orders_queue, deactive_orders_sql, add_orders_sql

    #calcute the range of orders
    if Type == 'sell':
        orders_range = (price, price*1.05)
        sign = 1
    else:
        orders_range = (price*0.95, price)
        sign = -1

    # get all active related orders
    orders = Order.objects.filter(user=ecryptom_user).filter(market=market).filter(active=True).filter(Type=Type)
    
    # deactivate orders that are out of range
    expired_orders = list(orders.filter(price__gt=orders_range[1]))
    expired_orders.extend(list(orders.filter(price__lt=orders_range[0])))
    for order in expired_orders:
        # add update command to deactive_orders_sql
        deactive_orders_sql += f'''
            ({order.id}, 
            \'{order.Type}\',
            {order.user.id},
            {order.market.id},
            {order.price},
            {order.total_amount},
            {order.traded_amount},
            \'{order.date.strftime("%Y-%m-%d %H:%M:%S")}\',
            \'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\',
            {0}),'''

        # print(f'''
        #    '-expire-'
        #    type : {Type}
        #    market : {market.name}
        #    price : {order.price}
        #    total_ammount: {order.total_amount}
        #    ''')
    
    # calcute the number of new orders that must generate
    count = number_of_orders - orders.count() + len(expired_orders)

    # if count < 0 then deactivate some orders
    if count < 0:
        active_orders = list(orders.filter(price__gt=orders_range[0]).filter(price__lt=orders_range[1]))
        for i in range(-count):
            order = active_orders.pop()
            # add update command to deactive_orders_sql
            deactive_orders_sql += f'''
                ({order.id}, 
                \'{order.Type}\',
                {order.user.id},
                {order.market.id},
                {order.price},
                {order.total_amount},
                {order.traded_amount},
                \'{order.date.strftime("%Y-%m-%d %H:%M:%S")}\',
                \'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\',
                {0}),'''

            # print(f'''
            # '--'
            # type : {Type}
            # market : {market.name}
            # price : {order.price}
            # total_ammount: {order.total_amount}
            # ''')
            
    #if count > 0 then generate new orders
    if count > 0:
        for i in range(count):
            o = Order(
                market=market,
                Type=Type,
                user=ecryptom_user,
                price= price * (1 + sign * random.random() * 0.05),
                total_amount=average_volume * (1 - random.random() * 0.9),
                expire_date= timezone.now() + timezone.timedelta(days=30)
            )
            # (Type, user_id, market_id, price, total_amount, traded_amount,date, expire_date, active)
            add_orders_sql += f'''
                (\'{Type}\',
                {ecryptom_user.id},
                {market.id},
                {price * (1 + sign * random.random() * 0.05)},
                {average_volume * (1 - random.random() * 0.9)},
                {0},
                \'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\',
                \'{(timezone.now()+timezone.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")}\',
                {1}
            ),'''
            # o.save()
            # Orders_queue(order=o).save()
            # print(f'''
            # '++'
            # type : {Type}
            # market : {market.name}
            # price : {o.price}
            # total_ammount: {o.total_amount}
            # ''')



toman = Currency.objects.get(symbol='TOMAN')
popular_currencies = ['BTC', 'ETH', 'USDT', 'BNB', 'BCH']

for market in Market.objects.filter(~Q(quote_currency=toman)):
    candle = One_min_candle.objects.filter(market=market).last()
    #print(f'start : {market.name}')
    try:
        # calcute the average volume (suppose the average is 1000 USDT)
        if market.quote_currency.symbol == 'USDT':
            average_volume = 1000 / candle.close_price 
        else:
            related_usdt_market = Market.objects.get(name=f'{candle.market.base_currency.symbol}USDT')
            price_in_USDT = One_min_candle.objects.filter(market=related_usdt_market).last().close_price
            average_volume = 1000 / price_in_USDT 

        if market.base_currency.symbol in popular_currencies:
            update_orders(market, candle.close_price, 'buy', average_volume, 7)
            update_orders(market, candle.close_price, 'sell', average_volume, 7)
        else:
            update_orders(market, candle.close_price, 'buy', average_volume, 2)
            update_orders(market, candle.close_price, 'sell', average_volume, 2)

    except Exception as e:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(market.name, e)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')



##################  save changes in db     ################

#  complete and execute the deactivation sql command
deactive_orders_sql = deactive_orders_sql[:-1] + ''' ON DUPLICATE KEY UPDATE 
    Type = VALUES(Type),
    user_id = VALUES(user_id),
    market_id = VALUES(market_id),
    price = VALUES(price),
    total_amount = VALUES(total_amount),
    traded_amount = VALUES(traded_amount),
    date = VALUES(date),
    expire_date=VALUES(expire_date),
    active = VALUES(active);
    '''
try:
    execute_sql(deactive_orders_sql)
except Exception as e:
    print(e)


# save last order id to identify new orders after that
last_order = Order.objects.filter(user=ecryptom_user).last()

# excomplete and execute the add order sql command
add_orders_sql = add_orders_sql[:-1] + ';'
try:
    execute_sql(add_orders_sql)
except Exception as e:
    print(e)


try:
    # add new orders to order_queue
    new_orders = Order.objects.filter(id__gt=last_order.id).filter(user=ecryptom_user)
    values = [f'({order.id})' for order in new_orders]
    values.pop()
    orders_queue_sql = f'insert into exchange_orders_queue (order_id) values {",".join(values)};'
    execute_sql(orders_queue_sql)
    # save last order with django orm to signal order_processor
    Orders_queue(order=new_orders.last()).save()
except Exception as e:
    print(e)

print('######################  finish  ############################')