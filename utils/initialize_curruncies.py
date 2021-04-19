import json
from exchange.models import Currency
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