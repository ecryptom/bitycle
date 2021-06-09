from django.urls import path
from .views import *

urlpatterns = [
    path('register', register.as_view()),
    path('login', login.as_view()),
    path('user_market_orders', user_market_orders.as_view()),
    path('user_active_market_orders', user_active_market_orders.as_view()),
]
