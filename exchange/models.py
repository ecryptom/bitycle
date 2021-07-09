from django.db import models
from decimal import Decimal, getcontext



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
    rank = models.IntegerField()

    def __str__(self):
        return self.name

class Market(models.Model):
    name = models.CharField(max_length=15)
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='market_as_base')
    quote_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='market_as_quote')
    def __str__(self):
        return self.name

    def get_info(self):
        last_1min_candle = One_min_candle.objects.filter(market=self).last()
        last_1day_candle = One_day_candle.objects.filter(market=self).last()
        return {
            'price': last_1min_candle.close_price,
            'daily_price_change_pct': self.base_currency.daily_price_change_pct,
            'market_cap': self.base_currency.market_cap,
            'high_daily_price': last_1day_candle.high_price,
            'low_daily_price': last_1day_candle.low_price
        }


class One_min_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField(default=0)

class Five_min_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField(default=0)

class Fifteen_min_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField(default=0)

class One_hour_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField(default=0)

class Four_hour_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField(default=0)

class One_day_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField(default=0)

class One_week_candle(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    open_time = models.IntegerField(db_index=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField(default=0)


class Order(models.Model):
    Type = models.CharField(max_length=4, choices=(('sell','sell'), ('buy','buy')))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    price = models.FloatField()
    total_amount = models.FloatField()
    traded_amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=True, db_index=True)
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='orders_as_base')
    quote_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='orders_as_quote')

    def remaining_amount(self):
        getcontext().prec = 10
        return float(Decimal(self.total_amount)-Decimal(self.traded_amount))

    def market_name(self):
        return self.market.name

    def average_traded_price(self):
        transactions = self.sales_transactions.all() if self.Type=='sell' else self.buy_transactions.all()
        if transactions:
            return sum([tran.price*tran.amount for tran in transactions]) / sum([tran.amount for tran in transactions])
        else:
            return 0

    def total_price(self):
        return self.total_amount * self.price
    

class Transaction(models.Model):
    seller_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sales_transactions')
    buyer_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='buy_transactions')
    buyer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='buys')
    seller = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='sales')
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    price = models.FloatField()
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class Orders_queue(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)


class Wallet(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='wallets')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='wallets')
    balance = models.FloatField(default=0)

    def blocked_balance(self):
        sell_orders = Order.objects.filter(active=True, user=self.user, Type='sell', base_currency=self.currency)
        buy_orders = Order.objects.filter(active=True, user=self.user, Type='buy', quote_currency=self.currency)
        s1 = sum([order.remaining_amount() for order in sell_orders])
        s2 = sum([order.remaining_amount()*order.price for order in buy_orders])
        return s1 + s2

    def non_blocked_balance(self):
        return self.balance - self.blocked_balance()

    class Meta:
        unique_together = ('user', 'currency',)

