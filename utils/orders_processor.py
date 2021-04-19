from exchange.models import Order, Transaction, Orders_queue


while True:
    try:
        head = Orders_queue.objects.first()

        if head:
            order = head.order
            print(order, 'start')
            if order.Type == 'buy':
                orders = Order.objects.filter(active=True).filter(Type='sell').filter(currency=order.currency).filter(base_currency=order.base_currency).filter(price__lte=order.price)
                orders = orders.order_by('price')
            elif order.Type == 'sell':
                orders = Order.objects.filter(active=True).filter(Type='buy').filter(currency=order.currency).filter(base_currency=order.base_currency).filter(price__gte=order.price)
                orders = orders.order_by('-price')
            remaining_amount = order.remaining_amount()

            #check adaptable orders and perform transactions
            for fit_order in orders:

                if fit_order.user == order.user:
                    continue 

                if fit_order.remaining_amount() <= remaining_amount:
                    Transaction(
                        currency=order.currency,
                        base_currency=order.base_currency,
                        price=order.price,
                        seller_order=order if order.Type=='sell' else fit_order,
                        buyer_order=order if order.Type=='buy' else fit_order,
                        seller=order.user if order.Type=='sell' else fit_order.user,
                        buyer=order.user if order.Type=='buy' else fit_order.user,
                        amount=fit_order.remaining_amount()
                    ).save()
                    print(f'''
                    amount : {fit_order.remaining_amount()}
                    price : {order.price}
                    seller order : {order if order.Type=='sell' else fit_order}
                    buyer order : {order if order.Type=='buy' else fit_order}
                    ''')
                    remaining_amount -= fit_order.remaining_amount()
                    fit_order.traded_amount = fit_order.total_amount
                    fit_order.active = False
                    fit_order.save()
                    
                else:
                    Transaction(
                        currency=order.currency,
                        base_currency=order.base_currency,
                        price=order.price,
                        seller_order=order if order.Type=='sell' else fit_order,
                        buyer_order=order if order.Type=='buy' else fit_order,
                        seller=order.user if order.Type=='sell' else fit_order.user,
                        buyer=order.user if order.Type=='buy' else fit_order.user,
                        amount=remaining_amount
                    ).save()
                    print(f'''
                    amount : {fit_order.remaining_amount()}
                    price : {order.price}
                    seller order : {order if order.Type=='sell' else fit_order}
                    buyer order : {order if order.Type=='buy' else fit_order}
                    ''')
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
        print('!!', e)