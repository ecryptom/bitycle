import requests
from bs4 import BeautifulSoup 
from exchange.models import Currency
from news.models import News
from datetime import datetime


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

resp=requests.get("https://arzdigital.com/breaking/",headers=headers)


soup = BeautifulSoup(resp.content)

# print(soup)
mydivs = soup.findAll('div',{'class':'arz-tab-content'})[0]
# print(mydivs)
dives=mydivs.findAll('div',{'class':'arz-col-sb-12 arz-col-md-sb-6 arz-col-lg-sb-4 arz-col-xxl-sb-3 arz-breaking-news__item'})
# print(dives)
for i in range(len(dives)):

    # scrap data from html page
    src_link=dives[i].findAll('a',{'class':'arz-breaking-news-post__source-link'})[0]['href']
    src_img=dives[i].findAll('a',{'class':'arz-breaking-news-post__source-link'})[0].findAll('img')[0]['src']
    src_name=dives[i].findAll('a',{'class':'arz-breaking-news-post__source-link'})[0].findAll('img')[0]['alt']
    title = dives[i].findAll('a',{'class':'arz-breaking-news__item-link arz-ignore-link'})[0]
    body=title.findAll('div',{'class':'arz-d-none arz-breaking-news__content'})[0]
    body_text=body.findAll('p')[0].contents[0]
    time=title.findAll('time')[0]['datetime']
    img=title.findAll('img')[0]['data-main-src']
    titlear=title['title']
    link_arzdg=title['href']
    data_post_id_arzdg=title['data-post-id']
    date_time_obj = datetime.strptime(time, '%Y-%m-%d')

    # break loop if finde a repeated article
    if News.objects.filter(post_id_arzdg=data_post_id_arzdg):
        break

    # convert sod_num if neccessery
    sod_num=title.findAll('div',{'class':'arz-breaking-news-post__info-rating-value'})[0].contents[0]
    if 'K' in str(sod_num):
        sod_num=int(float(str(sod_num).replace('K',''))*1000)
    zarar_num=title.findAll('div',{'class':'arz-breaking-news-post__info-rating-value'})[1].contents[0]
    if 'K' in str(zarar_num):
        zarar_num=int(float(str(zarar_num).replace('K',''))*1000)


    # save article
    news1=News(title=titlear, body=body_text, image=img, src_name=src_name, src_link=src_link, src_image=src_img, date=date_time_obj, pump=sod_num, dump=zarar_num, link_arzdg=link_arzdg, post_id_arzdg=data_post_id_arzdg)
    news1.save()

    # get related currencies from tags and add to news1
    try:        
        try:
            arz=dives[i].findAll('a',{'class':'arz-breaking-news-post__info-related-coins'})[0].findAll('img')
            for j in range(len(arz)):
                cr1=Currency.objects.get(name=str(arz[j]['alt']).lower())
                news1.currency.add(cr1)
        except:
            arz4=dives[i].findAll('div',{'class':'arz-breaking-news-post__info-related-coins'})[0].findAll('a',{'class':'arz-breaking-news-post__info-related-coin arz-tooltip'})
            for i in range(len(arz4)):
                arz = arz4[i].findAll('img')[0]['alt']
                cr1=Currency.objects.get(name=str(arz).lower())
                news1.currency.add(cr1)
    except Exception as e:
        print('error @2', e)
