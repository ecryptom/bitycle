from django.db import models
import json
from exchange.models import *


class Indicator(models.Model):
    strategy = models.ForeignKey('strategies.Strategy', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20)
    interval = models.CharField(max_length=3, choices=(('1m','1m'), ('5m','5m'), ('15m','15m'), ('1h','1h'), ('4h','4h'), ('1d', '1d'), ('1w','1w')))
    setup = models.TextField()
    line = models.CharField(max_length=20)
    value_type = models.CharField(max_length=10, choices=(('num','num'), ('candle','candle'), ('indicator','indicator')))
    value = models.CharField(max_length=50)
    action = models.CharField(max_length=15)
    
    def get_setup(self):
        return json.loads(self.setup)

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
    name = models.CharField(max_length=20)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    markets = models.ManyToManyField('exchange.Market')
    min_interval = models.CharField(max_length=3, choices=(('1m','1m'), ('5m','5m'), ('15m','15m'), ('1h','1h'), ('4h','4h'), ('1d', '1d'), ('1w','1w')))

        



class Candle_pattern(models.Model):
    
    name_en = models.CharField(max_length=20 ,null=True )
    name_fa = models.CharField(max_length=20)
    image = models.ImageField(upload_to='static/candle_pattern/image',null=True)
    kind = models.CharField(max_length=20, choices=(('single candle','single candle'), ('two candle','two candle'), ('three candle','three candle'), ('more candle','more candle')), null=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    markets = models.ManyToManyField('exchange.Market')
    patterns = models.TextField()
    interval = models.CharField(max_length=3, choices=(('1m','1m'), ('5m','5m'), ('15m','15m'), ('1h','1h'), ('4h','4h'), ('1d', '1d'), ('1w','1w')))

    def get_patterns(self):
        return json.loads(self.patterns)

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