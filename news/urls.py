from django.urls import path
from .views import *

urlpatterns = [
    path('market_news', market_news.as_view()),
]
