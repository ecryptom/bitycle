from django.db import models

class Currency(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10)
    persian_name = models.CharField(max_length=25)
    logo = models.ImageField(upload_to='logos', null=True)

class Base_currency(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10)
    persian_name = models.CharField(max_length=25)
    price = models.FloatField(default=1)
    logo = models.ImageField(upload_to='logos', null=True)
    reference = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.SET_NULL)


class One_min_candle(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='One_min_candles')
    open_time = models.IntegerField()
    close_time = models.IntegerField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField()
    number_of_trades = models.IntegerField()

class Five_min_candle(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='Five_min_candles')
    open_time = models.IntegerField()
    close_time = models.IntegerField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField()
    number_of_trades = models.IntegerField()

class One_day_candle(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='One_day_candles')
    open_time = models.IntegerField()
    close_time = models.IntegerField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField()
    number_of_trades = models.IntegerField()


class Order(models.Model):
    Type = models.CharField(max_length=4, choices=(('sell','sell'), ('buy','buy')))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    base_currency = models.ForeignKey(Base_currency, on_delete=models.CASCADE)
    price = models.FloatField()
    total_amount = models.FloatField()
    traded_amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    def remaining_amount(self):
        return self.total_amount - self.traded_amount
    

class Transaction(models.Model):
    seller_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sales_transactions')
    buyer_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='buy_transactions')
    buyer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='buys')
    seller = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='sales')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    base_currency = models.ForeignKey(Base_currency, on_delete=models.CASCADE)
    price = models.FloatField()
    amount = models.FloatField()
    date = models.DateTimeField(auto_now=True)


class Orders_queue(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)