import requests
from bs4 import BeautifulSoup 
from exchange.models import Currency
from news.models import News
from datetime import datetime
from utils.constant_variables import key_words
from django.db.models import Q


resp=requests.get("https://www.coinit.ir/category/news-article/")
soup = BeautifulSoup(resp.content,features="html.parser")

mydivs = soup.findAll('div',{'id':'masonry-grid'})[0]
dives=mydivs.findAll('div',{'class':'container-wrapper post-element tie-standard'})


for i in range(len(dives)):
    src_link = dives[i].findAll('h2',{'class':'entry-title'})[0].contents[0]['href']
    
    if News.objects.filter(src_link=src_link):
        break

    # scrap data from html page
    src_img = 'https://s19.picofile.com/d/8436842242/2e6393ca-ea5a-459c-93e6-7a314725d820/Coinit_Logo.svg'
    src_name = 'coinit'
    title = dives[i].findAll('h2',{'class':'entry-title'})[0].contents[0].text
    body = dives[i].findAll('p',{'class':'post-excerpt'})[0].contents[0]
    img = dives[i].findAll('img')[0]['src']
    date_time_obj = datetime.now()
    sod_num = 0
    zarar_num = 0

    ################### in news page ################
    resp = requests.get(src_link)
    soup = BeautifulSoup(resp.content,features="html.parser")
    mydiv = soup.findAll('div',{'id':'tie-wrapper'})[0]
    sub = mydiv.findAll('h2',{'class':'entry-sub-title'})[0].contents[0]
    txts = mydiv.findAll('p',{'style':'text-align: justify;'})+mydiv.findAll('div',{'class':'box-inner-block'})+mydiv.findAll('blockquote')
    msg = ''
    for txt in txts:
        msg += txt.text
    highlight = mydiv.findAll('div',{'id':'story-highlights'})[0].findAll('li')[0].contents[0]

    # save article
    news1=News(title=title, body=body, image=img, src_name=src_name, src_link=src_link, src_image=src_img, date=date_time_obj, pump=sod_num, dump=zarar_num)
    news1.save()

    txt = sub+msg+title
    for word in key_words:
        if word in txt:
            for cur in Currency.objects.filter(Q(name=word) | Q(persian_name=word) | Q(symbol=word)):
                news1.currency.add(cur)
