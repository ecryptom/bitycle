from django.urls import path
from .views import *

urlpatterns = [
    path('market_orders', market_orders.as_view()),
    path('send_order', send_order.as_view()),
    path('markets', markets.as_view()),
    path('market_currencies', market_currencies.as_view()),
    path('market_info', market_info.as_view()),
    path('market_transactions', market_transactions.as_view()),
]
