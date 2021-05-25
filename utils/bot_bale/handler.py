from bot import bot
from telepot.loop import MessageLoop
import redis
import telepot


redis_db = redis.Redis()

redis_db


members_id=[1436469837]
def handler(msg):
    global state,filter_list,filter_name,flag_rec,chat,obj_archive,mana,d
    count=0
    content_type, chat_type, chat_id = telepot.glance(msg)
    chat=chat_id
    print(content_type, chat_type, chat_id,msg['text'])
    if not chat_id in members_id:
        bot.sendMessage(chat_id,'به ربات bitycle خوش آمدید')
        members_id.append(chat_id)                               

MessageLoop(bot,handler).run_as_thread() 
print ('Listening ...')

while 1:
    pass