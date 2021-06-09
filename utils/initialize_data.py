import json
from exchange.models import Currency, Market, Wallet
from accounts.models import User
from utils.constant_variables import markets, currencies

############ initialize currencies  #####################
for cur in currencies:
    if not Currency.objects.filter(symbol=cur[1]):
        Currency(
            name = cur[0],
            symbol = cur[1],
            persian_name = cur[2],
            logo=cur[3],
            rank=cur[4]
        ).save()
        print(cur[0])

# add Toman to currencies
if not Currency.objects.filter(symbol='TOMAN'):
    Currency(
        name = 'toman',
        symbol = 'TOMAN',
        persian_name = 'تومان',
        logo= 'http://s6.picofile.com/file/8376555818/IRR.png',
    ).save()
    print(cur[0])




################ initialize markets  ######################
for market in markets:
    if not Market.objects.filter(name=market['name']):
        Market(
            name=market['name'],
            base_currency=Currency.objects.get(symbol=market['base']),
            quote_currency=Currency.objects.get(symbol=market['quote']),
        ).save()
        print(market['name'])


#################  initialize ecryptom_user  ################
if not User.objects.filter(username='ecryptom'):
    User(
        username='ecryptom',
        email='',
        phone='',
        verified_phone=True,
        name=''
    ).save()
    print('create ecryptom_user')

#################  initialize ecryptom_user wallet  ################
ecryptom_user = User.objects.get(username='ecryptom')
for cur in Currency.objects.all():
    if not Wallet.objects.filter(user=ecryptom_user, currency=cur):
        Wallet(
            user = ecryptom_user,
            currency = cur
        ).save()
        print(f'wallet {cur.name} for ecryptom_user')
