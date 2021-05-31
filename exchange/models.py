from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10)
    persian_name = models.CharField(max_length=25)
    logo = models.URLField(null=True)
    price = models.FloatField(default=0)
    daily_price_change_pct = models.FloatField(default=0)
    weekly_price_change_pct = models.FloatField(default=0)
    turnover = models.FloatField(default=0)
    market_cap = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Market(models.Model):
    name = models.CharField(max_length=15)
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='market_as_base')
    quote_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='market_as_quote')


class One_min_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()

class Five_min_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()

class Fifteen_min_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()

class One_hour_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()

class Four_hour_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()

class One_day_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()

class One_week_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()


class Order(models.Model):
    Type = models.CharField(max_length=4, choices=(('sell','sell'), ('buy','buy')))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    price = models.FloatField()
    total_amount = models.FloatField()
    traded_amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=True, db_index=True)
    def remaining_amount(self):
        return self.total_amount - self.traded_amount
    

class Transaction(models.Model):
    seller_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sales_transactions')
    buyer_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='buy_transactions')
    buyer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='buys')
    seller = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='sales')
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    price = models.FloatField()
    amount = models.FloatField()
    date = models.DateTimeField(auto_now=True)


class Orders_queue(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)


