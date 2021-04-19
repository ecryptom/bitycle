from exchange.models import Five_min_candle, Currency, Order, Transaction, Orders_queue
from accounts.models import User
from django.utils import timezone
import random

ecryptom_user = User.objects.get(username='ecryptom')
dollar = 25000


def update_orders(base_currency, Type, candle, number_of_orders):
    global Five_min_candle, Currency, Order, timezone, ecryptom_user, random, dollar, Orders_queue
    currency = candle.currency
    average_volume = candle.volume / candle.number_of_trades
    if Type == 'sell':
        orders_range = (candle.close_price, candle.close_price*1.05)
        sign = 1
    else:
        orders_range = (candle.close_price*0.95, candle.close_price)
        sign = -1

    #deactivate purchase orders that are out of range
    orders = Order.objects.filter(user=ecryptom_user).filter(base_currency=base_currency).filter(active=True).filter(Type=Type)
    expired_orders = list(orders.filter(price__gt=orders_range[1]))
    expired_orders.extend(list(orders.filter(price__lt=orders_range[0])))
    for order in expired_orders:
        order.active = False
        order.expire_date = timezone.now()
        order.save()
        print(f'''
            '-expire-'
            type : {Type}
            currency : {currency}
            price : {order.price}
            total_ammount: {order.total_amount}
            ''')
    
    #calcute the number of new orders that must generate
    count = number_of_orders - orders.count() + len(expired_orders)
    #if count < 0 then deactivate some orders
    if count < 0:
        active_orders = list(orders.filter(price__gt=orders_range[0]).filter(price__lt=orders_range[1]))
        for i in range(-count):
            order = active_orders.pop()
            order.active = False
            order.expire_date = timezone.now()
            order.save()
            print(f'''
            '--'
            type : {Type}
            currency : {currency}
            price : {order.price}
            total_ammount: {order.total_amount}
            ''')
    #if count > 0 then generate new orders
    if count > 0:
        for i in range(count):
            price = candle.close_price * (1 + sign * random.random() * 0.05)
            o = Order(
                currency=currency,
                Type=Type,
                user=ecryptom_user,
                base_currency=base_currency,
                price= price if base_currency=='USDT' else price*dollar,
                total_amount=average_volume * (1 - random.random() * 0.9),
                expire_date= timezone.now() + timezone.timedelta(days=30)
            )
            o.save()
            Orders_queue(order=o).save()
            print(f'''
            '++'
            type : {Type}
            currency : {currency}
            price : {o.price}
            total_ammount: {o.total_amount}
            ''')

update_orders('USDT','buy', Five_min_candle.objects.first(),20)
update_orders('USDT','sell', Five_min_candle.objects.first(),20)
update_orders('TOMAN','buy', Five_min_candle.objects.first(),20)
update_orders('TOMAN','sell', Five_min_candle.objects.first(),20)