import mysql.connector
from os import chdir
from defs import defs
from client import Client
import rooms
from collections import OrderedDict
import values

bot_token = values.bot_token()
my_user = values.me_token()
my_bot = defs(bot_token)

keyboard_game_init = [ [{'text' : 'دارایی ها' , 'command' : '//daraiy_ha'} , {'text' : 'جادو ها'   , 'command' : '//magics'   } ] , 
                       [{'text' : 'خروج از بازی' , 'command' : '//exit_game'}] ]

def game_loop (user_id):
    karakters = [
        'ادمکش' ,
        'راهزن' ,
        'تردست' ,
        'شاه'   ,
        'حکیم'  ,
        'تاجر'  ,
        'معمار' ,
        'سردار'
    ]
    server_loc = rooms.find_room(user_id)

    # مرحله حذف شدن کاراکتر اول
    x = my_bot.random_karakter()
    my_bot.send_group(server_loc , 'سیستم' , 'کاراکتر %s حذف شد' % x[0])
    karakters.remove(x[0])

    # مرحله نتخاب کاراکتر شانسی
    dict_user_karakter = OrderedDict()
    x = my_bot.random_karakter(karakters , 7)
    countertmp = 0

    with open (server_loc , 'r') as file:
        user_id_server = file.readlines()
        for har_user in user_id_server:
            har_user = har_user.strip()
            my_bot.send_message(har_user , 'کاراکتر شما هست: %s' % x[countertmp])
            dict_user_karakter[karakters[countertmp]] = har_user
            countertmp += 1

    # خود بازی
    my_bot.change_keyboard(my_user , keyboard_game_init)
    for message in my_bot.get_message():
        my_bot.change_keyboard(my_user , keyboard_game_init)
        print (message)
        if message['type'] == 'TEXT':
            if message['body'][0:2] == '//':
                vorodi = message['body']
                if vorodi == '//exit_game':
                    if my_bot.exit_game(user_id , server_loc):
                        my_bot.send_message(user_id , 'باموقیت از سرور خارج شدید')
                        my_bot.send_group(server_loc , 'سیستم' , 'کاربر %s از بازی خارج شد' % user_id)
                        break
                if vorodi == '//magics':
                    my_bot.magics_game(user_id)
                if vorodi == '//daraiy_ha':
                    my_bot.daraiy_ha_game(user_id)
                my_bot.change_keyboard(user_id , keyboard_game_init)
                # اجرا کردن دستور کیبورد
            else:
                my_bot.send_group(server_loc , 'test' , message['body'])




game_loop(my_user)

