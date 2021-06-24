import requests
from bs4 import BeautifulSoup 
from exchange.models import Currency
from news.models import News
from datetime import datetime
from utils.constant_variables import key_words
from django.db.models import Q


headers = {
# 'Host': 'arzdigital.com',
'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language':'en-US,en;q=0.5',
# 'Accept-Encoding': 'gzip, deflate, br',
'Connection':'keep-alive',
'Cookie': 'atlas-offer=true; __arzpush-time-cookie=1646040640054; _ga_1WTFY992R9=GS1.1.1621768598.3.1.1621768941.0; _ga=GA1.2.769233558.1621760911; _gid=GA1.2.321327537.1621760916; _scroll=true; PHPSESSID=e481cee613538211ae116d8f1342983a; _gat_UA-191729093-1=1',
'Upgrade-Insecure-Requests': '1',
'Pragma':'no-cache',
'Cache-Control': 'no-cache'}

resp=requests.get("https://arzdigital.com/category/news/",headers=headers)
soup = BeautifulSoup(resp.content,features="html.parser")

mydivs = soup.findAll('div',{'class':'arz-row-sb arz-posts'})[0]
dives=mydivs.findAll('a',{'class':'arz-last-post arz-row'})

for i in range(len(dives)):

    src_link=dives[i]['href']

    # break loop if finde a repeated article
    if News.objects.filter(src_link=src_link):
        break

    print(src_link)
    src_img = 'arzdigital.png'
    src_name = 'arzdigital'
    title = dives[i]['title']

    img = dives[i].findAll('img')[0]['data-src']
    sub = dives[i].findAll('div',{'class':'arz-last-post__text'})[0].findAll('p')[0].contents[0]
    date_time_obj = datetime.now()
    sod_num = 0
    zarar_num = 0

    ################### in news page ################
    resp=requests.get(src_link)
    soup = BeautifulSoup(resp.content,features="html.parser")

    mydiv = soup.findAll('section',{'class':'arz-post__content'})[0].findAll('p')
    msg = ''
    for txt in mydiv[:-1]:
        msg += txt.text

    # save article
    news1=News(title=title, body=msg, image=img, src_name=src_name, src_link=src_link, src_image=src_img, date=date_time_obj, pump=sod_num, dump=zarar_num, link_arzdg=src_link)
    news1.save()

    txt = sub+msg+title
    for word in key_words:
        if word in txt:
            for cur in Currency.objects.filter(Q(name=word) | Q(persian_name=word) | Q(symbol=word)):
                news1.currency.add(cur)
