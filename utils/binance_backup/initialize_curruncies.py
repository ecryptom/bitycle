import json
from exchange.models import Currency, Base_currency
from accounts.models import User

curs = json.load(open('utils/new_nomics_list.txt'))

for cur in curs:
    Currency(
        name = cur[0],
        symbol = cur[1],
        persian_name = cur[2]
    ).save()
    print(cur[0])

#initialize ecryptom_user
User(
    username='ecryptom',
    email='',
    phone='',
    verified_phone=True,
    name=''
).save()



#initialize base_currencies
curs = [["bitcoin", "BTC", "\u0628\u06cc\u062a \u06a9\u0648\u06cc\u0646", "https://cdn.arzdigital.com/uploads/assets/coins/icons/bitcoin.png"], ["ethereum", "ETH", "\u0627\u062a\u0631\u06cc\u0648\u0645", "https://cdn.arzdigital.com/uploads/assets/coins/icons/ethereum.png"], ["tether", "USDT", "\u062a\u062a\u0631", "https://cdn.arzdigital.com/uploads/assets/coins/icons/tether.png"], ["xrp", "XRP", "\u0631\u06cc\u067e\u0644", "https://cdn.arzdigital.com/uploads/assets/coins/icons/xrp.png"], ["litecoin", "LTC", "\u0644\u0627\u06cc\u062a \u06a9\u0648\u06cc\u0646", "https://cdn.arzdigital.com/uploads/assets/coins/icons/litecoin.png"]]
for cur in curs:
    if Base_currency.objects.filter(symbol=cur[1]):
        continue
    Base_currency(
        name = cur[0],
        symbol = cur[1],
        persian_name = cur[2],
        price = 1,
        reference=Currency.objects.get(symbol=cur[1])
    ).save()
    print(cur[1])
#add toman
if not Base_currency.objects.filter(symbol='TOMAN'):
    Base_currency(
        name = 'TOMAN',
        symbol = 'TOMAN',
        persian_name = 'تومان',
        price = 1,
    ).save()