from django.urls import path
from .views import *

urlpatterns = [
    path('market_orders', market_orders.as_view()),
    path('send_order', send_order.as_view()),
]
