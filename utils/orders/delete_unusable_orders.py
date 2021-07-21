from exchange.models import Currency, Order, Orders_queue, Market, Transaction
from accounts.models import User
from django.utils import timezone
import random
from django.db.models import Q
from utils.mysql_engine import execute_sql
from datetime import datetime


ecryptom_user = User.objects.get(username='ecryptom')

usable_orders_id = {order.id:0 for order in Order.objects.filter(user=ecryptom_user, active=True)}
for trans in Transaction.objects.all():
    usable_orders_id[trans.seller_order.id] = 0
    usable_orders_id[trans.buyer_order.id] = 0


    
inactive_ecryptom_orders = Order.objects.filter(user=ecryptom_user, active=False)

for order in inactive_ecryptom_orders:
    if order.id not in usable_orders_id:
        print(order)
        order.delete()