from django.urls import path
from .views import *

urlpatterns = [
    path('save_candles', save_candles.as_view()),
]
