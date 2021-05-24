from exchange.models import Order, Transaction, Orders_queue
from django.db.models.signals import post_save
import redis

redis_db = redis.Redis()
redis_db.set('is_active', 'False')

def process(sender, instance, **kwargs):

    # exit if another process is handelling orders
    if redis_db.get('is_active') == b'True':
        return 0

    redis_db.set('is_active', 'True')

    try:

        head = Orders_queue.objects.first()

        while head:
            try:
                order = head.order
                #print(order, 'start')
                if order.Type == 'buy':
                    orders = Order.objects.filter(active=True, Type='sell', market=order.market, price__lte=order.price)
                    orders = orders.order_by('price')
                elif order.Type == 'sell':
                    orders = Order.objects.filter(active=True, Type='sell', market=order.market, price__lte=order.price)
                    orders = orders.order_by('-price')
                remaining_amount = order.remaining_amount()

                #check adaptable orders and perform transactions
                for fit_order in orders:

                    if fit_order.user == order.user and order.user.username=='ecryptom':
                        continue 

                    if fit_order.remaining_amount() <= remaining_amount:
                        Transaction(
                            market=order.market,
                            price=order.price,
                            seller_order=order if order.Type=='sell' else fit_order,
                            buyer_order=order if order.Type=='buy' else fit_order,
                            seller=order.user if order.Type=='sell' else fit_order.user,
                            buyer=order.user if order.Type=='buy' else fit_order.user,
                            amount=fit_order.remaining_amount()
                        ).save()
                        # print(f'''
                        # amount : {fit_order.remaining_amount()}
                        # price : {order.price}
                        # market : {order.market.name}
                        # seller order : {order if order.Type=='sell' else fit_order}
                        # buyer order : {order if order.Type=='buy' else fit_order}
                        # ''')
                        remaining_amount -= fit_order.remaining_amount()
                        fit_order.traded_amount = fit_order.total_amount
                        fit_order.active = False
                        fit_order.save()

                    else:
                        Transaction(
                            market=order.market,
                            price=order.price,
                            seller_order=order if order.Type=='sell' else fit_order,
                            buyer_order=order if order.Type=='buy' else fit_order,
                            seller=order.user if order.Type=='sell' else fit_order.user,
                            buyer=order.user if order.Type=='buy' else fit_order.user,
                            amount=remaining_amount
                        ).save()
                        # print(f'''
                        # amount : {remaining_amount}
                        # price : {order.price}
                        # market : {order.market.name}
                        # seller order : {order if order.Type=='sell' else fit_order}
                        # buyer order : {order if order.Type=='buy' else fit_order}
                        # ''')
                        fit_order.traded_amount += remaining_amount
                        fit_order.save()
                        remaining_amount = 0
                        break

                order.remaining_amount = remaining_amount
                order.traded_amount = order.total_amount - remaining_amount
                order.active = remaining_amount > 0
                order.save()
                head.delete()

            except Exception as e:
                print('!!!!!!!!!!!!!!!', e)

            # get head of queue to check in while condition
            head = Orders_queue.objects.first()

    except:
        pass  

    redis_db.set('is_active', 'False')



post_save.connect(process, sender=Orders_queue)
