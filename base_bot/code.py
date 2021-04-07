from os import chdir
chdir('base_bot/')
from collections import OrderedDict
from defs import defs
import values
from user import user
from rooms import room

bot = defs(values.bot_token())

def main_page (karbar:user):

    my_bot = defs(values.bot_token())
    user_id = karbar.ID
    main_page_keyboard_init = values.main_page_keyboard_init()
    init_message = 'سلام %s عزیز\n لطفا بین گزینه ها انتخاب کن تا من جواب بدم' % karbar.name

    for message in my_bot.get_message():
        if message['from'] == user_id:
            init_message = 'سلام %s عزیز\n لطفا بین گزینه ها انتخاب کن تا من جواب بدم' % karbar.name

            if message['type'] == 'TEXT':
                txt = message['body']
                if txt == '//start_game_main_page':
                    my_bot.start_game(karbar)
                if txt == '//change_name_main_page':
                    if my_bot.change_name(karbar):
                        karbar.update_values()
                if txt == '//amtiaz_ha_main_page':
                    my_bot.amtiaz_hai_karbar(karbar)
                if txt == '//delete_data_main_page':
                    if my_bot.reset_rank(user_id):
                        karbar = user(user_id)
                if txt == '//best_gamer_main_page':
                    my_bot.show_best_gamer(karbar , main_page_keyboard_init)
                if txt == '//help_about_game':
                    my_bot.help_about_game(karbar , main_page_keyboard_init)
                my_bot.change_keyboard(user_id , main_page_keyboard_init)

            else:
                my_bot.send_message(user_id , 'متاسفم لطفا فقط از حروف استفاده کنید و یا از کیبورد کمک بگیرید' , main_page_keyboard_init)

            my_bot.send_message(user_id , init_message , main_page_keyboard_init)

def game_loop (karbar:user):

    # values
    karakters = values.karakters_game_loop()
    dict_user_karakter = OrderedDict()
    my_bot = defs(values.bot_token())
    keyboard_game_init = values.game_loop_keyboard_init()
    user_id = karbar.ID

    SQL = values.sql_connect()
    cursor = SQL.cursor()
    server = room(karbar)
    server_loc = server.server_loc

    # مرحله حذف شدن کاراکتر اول
    x = my_bot.random_karakter()
    my_bot.send_group(server_loc , 'سیستم' , 'کاراکتر %s حذف شد' % x[0])
    karakters.remove(x[0])

    # مرحله انتخاب کاراکتر شانسی
    x = my_bot.random_karakter(karakters , 7)
    c = 0

    cursor.execute('SELECT ID FROM %s' % server_loc)
    users_id_server = cursor.fetchall()
    for har_user in users_id_server:
        my_bot.send_message(har_user[0] , 'کاراکتر شما هست: %s' % x[c])
        dict_user_karakter[karakters[c]] = har_user
        c += 1

    # خود بازی
    my_bot.change_keyboard(user_id , keyboard_game_init)
    for message in my_bot.get_message():
        my_bot.change_keyboard(user_id , keyboard_game_init)
        if message['from'] == user_id:
            if message['type'] == 'TEXT':
                if message['body'][0:2] == '//':
                    # اجرا کردن دستور کیبورد
                    vorodi = message['body']
                    if vorodi == '//exit_game':
                        if my_bot.exit_game(user_id , server_loc):
                            my_bot.send_message(user_id , 'باموقیت از سرور خارج شدید')
                            tmp_message = 'کاربر %s از بازی خارج شد و شهرش نابود شد' % karbar.name
                            my_bot.send_group(server_loc , 'سیستم' , tmp_message)
                            main_page(karbar)
                    if vorodi == '//magics':
                        my_bot.magics_game(user_id)
                    if vorodi == '//daraiy_ha':
                        my_bot.daraiy_ha_game(user_id , server)
                    my_bot.change_keyboard(user_id , keyboard_game_init)
                else:
                    my_bot.send_group(server_loc , karbar.name , message['body'] , keyboard_game_init)
            else:
                my_bot.send_message(user_id , 'فرمت پیام صحیح نیست' , keyboard_game_init)

for message in bot.get_message():
    game_loop(user(message['from']))
