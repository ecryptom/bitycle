from django.db import models
import json
from exchange.models import *


class Indicator(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    strategy = models.ForeignKey('strategies.Strategy', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20)
    interval = models.CharField(max_length=3, choices=(('1m','1m'), ('5m','5m'), ('15m','15m'), ('1h','1h'), ('4h','4h'), ('1d', '1d'), ('1w','1w')))
    setup = models.TextField()
    lines = models.TextField()
    last_status = models.TextField(default='{}')

    def get_setup(self):
        return json.loads(self.setup)

    def get_lines(self):
        return json.loads(self.lines)

    def get_candle_class(self):
        if self.interval == '1m':
            return One_min_candle
        if self.interval == '5m':
            return Five_min_candle
        if self.interval == '15m':
            return Fifteen_min_candle
        if self.interval == '1h':
            return One_hour_candle
        if self.interval == '4h':
            return Four_hour_candle
        if self.interval == '1d':
            return One_day_candle
        if self.interval == '1w':
            return One_week_candle
        

class Strategy(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    

