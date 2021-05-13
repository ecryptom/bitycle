from exchange.models import Five_min_candle, Currency, Order, Orders_queue, Base_currency
from accounts.models import User
from django.utils import timezone
import random

ecryptom_user = User.objects.get(username='ecryptom')
dollar = 25000

# price => price of currency (price of base_currency is available in its instance)
# average_volume => the average volume of all trades in last candel (candel.volume / candel.number_of_trades)
# number_of_orders => number of orders you want to be on trades table (by ecryptom_user)

def update_orders(base_currency, currency, price, Type, average_volume, number_of_orders):
    global Five_min_candle, Currency, Order, timezone, ecryptom_user, random, dollar, Orders_queue, Base_currency

    # do not create any order if currency is as same as order base_currency
    if currency == base_currency.reference:
        return 0

    # change base_currency from USDT to our desired base_currency
    price = price / base_currency.price

    #calcute the range of orders
    if Type == 'sell':
        orders_range = (price, price*1.05)
        sign = 1
    else:
        orders_range = (price*0.95, price)
        sign = -1

    # get all active related orders
    orders = Order.objects.filter(user=ecryptom_user).filter(currency=currency).filter(base_currency=base_currency).filter(active=True).filter(Type=Type)
    
    # deactivate orders that are out of range
    expired_orders = list(orders.filter(price__gt=orders_range[1]))
    expired_orders.extend(list(orders.filter(price__lt=orders_range[0])))
    for order in expired_orders:
        order.active = False
        order.expire_date = timezone.now()
        order.save()
        print(f'''
            '-expire-'
            type : {Type}
            currency : {currency.symbol}
            price : {order.price}
            base_currency : {base_currency.symbol}
            total_ammount: {order.total_amount}
            ''')
    
    # calcute the number of new orders that must generate
    count = number_of_orders - orders.count() + len(expired_orders)

    # if count < 0 then deactivate some orders
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
            currency : {currency.symbol}
            base_currency : {base_currency.symbol}
            price : {order.price}
            total_ammount: {order.total_amount}
            ''')
    #if count > 0 then generate new orders
    if count > 0:
        for i in range(count):
            o = Order(
                currency=currency,
                Type=Type,
                user=ecryptom_user,
                base_currency=base_currency,
                price= price * (1 + sign * random.random() * 0.05),
                total_amount=average_volume * (1 - random.random() * 0.9),
                expire_date= timezone.now() + timezone.timedelta(days=30)
            )
            o.save()
            Orders_queue(order=o).save()
            print(f'''
            '++'
            type : {Type}
            currency : {currency.symbol}
            price : {o.price}
            base_currency : {base_currency.symbol}
            total_ammount: {o.total_amount}
            ''')

for base_currency in Base_currency.objects.all():
    for currency in Currency.objects.all():
        candle = Five_min_candle.objects.filter(currency=currency).last()
        print(f'start : {currency.symbol} _ {base_currency.symbol}')
        if base_currency.reference != currency:
            try:
                update_orders(base_currency, currency, candle.close_price, 'buy', candle.volume/candle.number_of_trades, 2)
                update_orders(base_currency, currency, candle.close_price, 'sell', candle.volume/candle.number_of_trades, 2)
            except:
                print(currency.symbol, base_currency.symbol)
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

print('fi')