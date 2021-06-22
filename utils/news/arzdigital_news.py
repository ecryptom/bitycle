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

resp=requests.get("https://arzdigital.com/category/news/",headers=headers)


soup = BeautifulSoup(resp.content,features="html.parser")

# print(soup)
mydivs = soup.findAll('div',{'class':'arz-row-sb arz-posts'})[0]
# print(mydivs)
dives=mydivs.findAll('a',{'class':'arz-last-post arz-row'})
# print(dives[0])
# for i in range(len(dives)):
for i in range(len(dives)-1,len(dives)):

    src_link=dives[i]['href']

    # # break loop if finde a repeated article
    if News.objects.filter(src_link=src_link):
        break

    # print(src_link)
    src_img='arzdigital'
    src_name='arzdigital.png'
    title = dives[i]['title']

    img=dives[i].findAll('img')[0]['data-src']
    # print(img)
    sub=dives[i].findAll('div',{'class':'arz-last-post__text'})[0].findAll('p')[0].contents[0]
    # print(sub)
    date_time_obj = datetime.now()
    sod_num=0
    zarar_num=0

    ################### in news page ################

    resp=requests.get(src_link)

    soup = BeautifulSoup(resp.content,features="html.parser")

    # print(soup)
    mydiv = soup.findAll('section',{'class':'arz-post__content'})[0].findAll('p')
    # print(mydiv)
    msg=''
    # print(txts)
    for txt in mydiv[:-1]:
        msg+=txt.text

    # print(msg)


    # # save article
    # news1=News(title=titlear, body=body_text, image=img, src_name=src_name, src_link=src_link, src_image=src_img, date=date_time_obj, pump=sod_num, dump=zarar_num, link_arzdg=link_arzdg, post_id_arzdg=data_post_id_arzdg)
    # news1.save()

    # # get related currencies from tags and add to news1
    # try:        
    #     try:
    #         arz=dives[i].findAll('a',{'class':'arz-breaking-news-post__info-related-coins'})[0].findAll('img')
    #         for j in range(len(arz)):
    #             cr1=Currency.objects.get(name=str(arz[j]['alt']).lower())
    #             news1.currency.add(cr1)
    #     except:
    #         arz4=dives[i].findAll('div',{'class':'arz-breaking-news-post__info-related-coins'})[0].findAll('a',{'class':'arz-breaking-news-post__info-related-coin arz-tooltip'})
    #         for i in range(len(arz4)):
    #             arz = arz4[i].findAll('img')[0]['alt']
    #             cr1=Currency.objects.get(name=str(arz).lower())
    #             news1.currency.add(cr1)
    # except Exception as e:
    #     print('error @2', e)
