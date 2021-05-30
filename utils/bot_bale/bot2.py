
import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,InlineQueryResultVideo,ReplyKeyboardMarkup,KeyboardButton
# import logging
bale_token = "260752710:465bea46b20c3775bf21df37a983a2909f99f393"

telegram_token = "1714627889:AAEI5Va3thmvwvbR5bJWY7GisoKMgJv1YQQ"
bot=telebot.TeleBot(token=bale_token)
usernamearr={'safari78':'12345','manman':'4420886048'}

# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

username_input=''
# password_eror=0

def markup_signup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("ثبت نام",url='www.bitycle.com/register'))
    return markup

def markup_forget_pass():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("فراموشی رمز عبور",url='www.bitycle.com/forgetpassword' ,callback_data="forgetpassword"))
    return markup

def markup_signup_bott():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = InlineKeyboardButton("ثبت نام",url='www.bitycle.com/register')
    itembtn2 = KeyboardButton('ورود')
    markup.add(itembtn1, itembtn2)

    return markup

def markup_menu():

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width=2
    itembtn1 = KeyboardButton('استراتژی ها📊')
    itembtn2 = KeyboardButton('نبض بازار📈')
    itembtn4 = KeyboardButton('دستیاربازار🤖')
    itembtn3 = KeyboardButton('تنظیمات⚙️')
    itembtn5 = KeyboardButton('راهنما🔖')
    markup.add(itembtn1, itembtn2,itembtn3,itembtn4,itembtn5)

    return markup
def strategy_menu():

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width=2
    itembtn1 = KeyboardButton('مشاهده استراتژی ها📊')
    itembtn2 = KeyboardButton('ویرایش استراتژی ها ✏️')
    itembtn3 = KeyboardButton('برگشت ↪️')

    markup.add(itembtn1, itembtn2,itembtn3)

    return markup
def nabz_menu():

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width=2
    itembtn1 = KeyboardButton('مشاهده قیمت💰')
    itembtn2 = KeyboardButton('مشاهده تابلو و چارت 📊')
    itembtn3 = KeyboardButton('فیلتر صعودی و نزولی 📈')
    itembtn4 = KeyboardButton('برگشت ↪️')

    markup.add(itembtn1, itembtn2,itembtn4,itembtn3)

    return markup
def assis_menu():

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width=2
    itembtn1 = KeyboardButton('دستیار تکنیکال📈')
    itembtn2 = KeyboardButton('دستیار فاندامنتال📡')
    itembtn3 = KeyboardButton('دستیار بایننس💵')
    itembtn4 = KeyboardButton('برگشت ↪️')

    markup.add(itembtn1, itembtn2,itembtn4,itembtn3)

    return markup
def notif_menu():

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width=2
    itembtn1 = KeyboardButton('تنظیم اعلان ها🔔')
    itembtn2 = KeyboardButton('برگشت ↪️')

    markup.add(itembtn2,itembtn1)

    return markup

def give_username(message):
    if (message.text) in usernamearr.keys():
        username_input=message.text

        # print(username_input)
        start_msg='لطفا رمز عبور خودرا  وارد نمایید'
        sent=bot.send_message(message.chat.id, start_msg)
        bot.register_next_step_handler(sent,give_password, username_input)
    elif 'ثبت نام' in message.text:
        start_msg=f' سلام {message.from_user.username} عزیز❤   ️ \n\n از طریق لینک زیر اقدام به ثبت نام در سایت نمایید'
        bot.send_message(message.chat.id, start_msg , reply_markup=markup_signup())
    else :
        start_msg='لطفا  نام کاربری صحیح را وارد نمایید'
        sent=bot.send_message(message.chat.id, start_msg)
        bot.register_next_step_handler(sent,give_username)

def give_password(message,username_input):
    print(usernamearr[f'{username_input}'],message.text,username_input)
    if   message.text== usernamearr[f'{username_input}']:
        pass_input=message.text
        # print(pass_input)
        start_msg='خوش آمدید🌹\n  از منوی زیر بخش مورد نظر خودرا انتخاب کنید.'
        bot.send_message(message.chat.id, start_msg,reply_markup=markup_menu())
    elif 'ثبت نام' in message.text:
        start_msg=f' سلام {message.from_user.username} عزیز❤   ️ \n\n از طریق لینک زیر اقدام به ثبت نام در سایت نمایید'
        bot.send_message(message.chat.id, start_msg , reply_markup=markup_signup())

    else:
        start_msg='لطفا رمز عبور صحیح را وارد نمایید'
        sent=bot.send_message(message.chat.id, start_msg)
        bot.register_next_step_handler(sent,give_password, username_input)

def setting(message):
    if  'برگشت' in message.text:
        start_msg='لطفا از منو زیر انتخاب نمایید'
        sent=bot.send_message(message.chat.id, start_msg,reply_markup=markup_menu())
def assis(message):
    if  'برگشت' in message.text:
        start_msg='لطفا از منو زیر انتخاب نمایید'
        sent=bot.send_message(message.chat.id, start_msg,reply_markup=markup_menu())
def notif(message):
    if  'برگشت' in message.text:
        start_msg='لطفا از منو زیر انتخاب نمایید'
        sent=bot.send_message(message.chat.id, start_msg,reply_markup=markup_menu())
def strategy(message):
    if  'برگشت' in message.text:
        start_msg='لطفا از منو زیر انتخاب نمایید'
        sent=bot.send_message(message.chat.id, start_msg,reply_markup=markup_menu())
def nabz(message):
    if  'برگشت' in message.text:
        start_msg='لطفا از منو زیر انتخاب نمایید'
        sent=bot.send_message(message.chat.id, start_msg,reply_markup=markup_menu())

@bot.message_handler(func=lambda message: True)
def send_welcomes(message):
    global state,username_input
    if 'start' in message.text:
        start_msg=f' سلام {message.from_user.username} عزیز❤   ️ \n\n به ربات هوشمند 🎖️بایتیکل🎖️ خوش اومدی\n اگه هنوز توی سایت ما\n🌐 www.bitycle.com \n\n ثبت نام نکردی اول از طریق دکمه زیر ثبتنام کن'
        bot.send_message(message.chat.id, start_msg,reply_markup=markup_signup_bott())
    if 'help' in message.text:
        msg1='در این ربات علاوه بر دریافت اعلان های لحظه ای استراتژی های سایت و اطلاع از اشتباهات معاملات سیستم شبیه ساز, میتونی توی ربات بایتیکل از خدمات زیر استفاده کنید \n\n'
        msg2='📈نبض بازار\n -مشاهده قیمت لحظه ای بیش از 400 بازار\n-مشاهده تابلو و چارت بیش از 400 بازار\n -مشاهده صعودی و نزولی ترین مارکتها \n\n'
        msg3='📊استراتژی ها\n -مشاهده استراتژی ها فعال\n -حذف استراتژی های فعال \n\n '
        msg4='🤖دستیاربازار\n -دستیار تکنیکال \n -دستیار فاندامنتال و مشاهده اخرین اخبار مارکتها \n -دستیار بایننس و مشاهده وضعیت سفارشات \n\n'
        msg5='⚙️ تنظیمات\n -تنظیمات اعلان ها'
        start_msg=f' سلام {message.from_user.username} عزیز❤   ️ \n\n به ربات هوشمند 🎖️بایتیکل🎖️ خوش اومدی' +'\n\n'+msg1
        start_msg1=msg2+msg3+msg4+msg5
        bot.send_message(message.chat.id, start_msg,)
        bot.send_message(message.chat.id, start_msg1,)
    if 'راهنما' in message.text:
        msg1='در این ربات علاوه بر دریافت اعلان های لحظه ای استراتژی های سایت و اطلاع از اشتباهات معاملات سیستم شبیه ساز شما میتونید توی ربات بایتیکل از خدمات زیر استفاده کنید \n\n'
        msg2='📈نبض بازار\n -مشاهده قیمت لحظه ای بیشش از 400 بازار\n-مشاهده تابلو و چارت بیشش از 400 بازار\n -مشاهده صعودی و نزولی ترین مارکتها \n\n'
        msg3='📊استراتژی ها\n -مشاهده استراتژی ها فعال\n -حذف استراتژی های فعال \n\n '
        msg4='🤖دستیاربازار\n -دستیار تکنیکال \n -دستیار فاندامنتال و مشاهده اخرین اخبار مارکتها \n -دستیار بایننس و مشاهده وضعیت سفارشات \n\n'
        msg5='⚙️ تنظیمات\n -تنظیمات اعلان ها'
        start_msg=f' سلام {message.from_user.username} عزیز❤   ️ \n\n به ربات هوشمند 🎖️بایتیکل🎖️ خوش اومدی' +'\n\n'+msg1
        start_msg1=msg2+msg3+msg4+msg5
        bot.send_message(message.chat.id, start_msg,)
        bot.send_message(message.chat.id, start_msg1,)
    if 'ثبت نام' in message.text:
        start_msg=f' سلام {message.from_user.username} عزیز❤   ️ \n\n از طریق لینک زیر اقدام به ثبت نام در سایت نمایید'
        bot.send_message(message.chat.id, start_msg , reply_markup=markup_signup())
    if 'ورود' in message.text:
        start_msg='لطفا نام کاربری خودرا  وارد نمایید'
        sent=bot.send_message(message.chat.id, start_msg)
        bot.register_next_step_handler(sent,give_username)
    if 'دستیاربازار' in message.text:
        start_msg='لطفا از منو زیر انتخاب نمایید'
        sent=bot.send_message(message.chat.id, start_msg,reply_markup=assis_menu())
        bot.register_next_step_handler(sent,assis)
    if 'استراتژی ها' in message.text:
        start_msg='لطفا از منو زیر انتخاب نمایید'
        sent=bot.send_message(message.chat.id, start_msg,reply_markup=strategy_menu())
        bot.register_next_step_handler(sent,strategy)
    if 'نبض بازار' in message.text:
        start_msg='لطفا از منو زیر انتخاب نمایید'
        sent=bot.send_message(message.chat.id, start_msg,reply_markup=nabz_menu())
        bot.register_next_step_handler(sent,nabz)
    if 'تنظیمات' in message.text:
        start_msg='لطفا از منو زیر انتخاب نمایید'
        sent=bot.send_message(message.chat.id, start_msg,reply_markup=notif_menu())
        bot.register_next_step_handler(sent,setting)

# bot.polling(none_stop=True)



# @bot.callback_query_handler(func=lambda call: True)
# def  test_callback(call):
#     print(call.contact)
#     # logger.info(call.contact)
#         # usernameget()
#     #     @bot.message_handler(func=lambda message: True)
#     #     def username(message):
#     # # print(message.from_user.username)
#     #         msg=message.text
#     #         print(msg)
#     #         bot.send_message(message.chat.id, 'password?')

#         # bot.answer_callback_query(call.id, "voroddd")

















# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     if message.text=='/start':
#         # bot.reply_to(message, 'به ربات هوشمند bitycle خوش امدید')
# @bot.inline_handler(lambda query: query.query == 'video')
# def query_video(inline_query):
#     try:
#         r = InlineQueryResultVideo('1',
#                                          'https://github.com/eternnoir/pyTelegramBotAPI/blob/master/tests/test_data/test_video.mp4?raw=true',
#                                          'video/mp4', 'Video',
#                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',
#                                          'Title'
#                                          )
#         bot.answer_inline_query(inline_query.id, [r])
#     except Exception as e:
#         print(e)



# def gen_markup():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 2
#     markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
#                                InlineKeyboardButton("No", callback_data="cb_no"))
#     return markup

# def usernameget(message):
#     bot.send_message(message.chat.id, "username?")


# @bot.message_handler(func=lambda message: True)
# def message_handler(message):
#     bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())



while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)



