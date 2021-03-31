from defs import defs
import values
from user import user

def create_user(user_id):
    SQL = values.sql_connect()
    bot = defs(values.bot_token())
    cursor = SQL.cursor()
    bot.send_message(user_id , 'متاسفانه اسم شما در بازی ثبت نشده است لطفا اسم خود را وارد نمایید')

    for message in bot.get_message():
        print (message)
        if message['from'] == user_id:
            if message['body'] == '//yes_create_user_name':
                cursor.execute('INSERT INTO Users (ID  , Name) VALUES ("%s" , "%s")' % (user_id , name_karbar))
                bot.send_message(user_id , 'حالا دیگه عضو بازی شدی می تونی وارد بازی بشی و بقیه رو دعوت کنی تا سکه بگیری \n راستی ۲۰ تا سکه هم برای عضو شدنت به حسابت اضافه شد')
                SQL.commit()
                cursor.execute('SELECT * FROM Users WHERE ID="%s"' % (user_id))
                return cursor.fetchall()[0]

            name_karbar = message['body']
            tmp_message = 'اسم شما %s هست دیگه نه؟' % name_karbar
            tmp_keyboard = [[{'text' : 'اره همینه' , 'command' : '//yes_create_user_name'} , {'text' : 'نه اشتباهه' , 'command' : '//no_create_bot_name'}]]

            bot.send_message(user_id , tmp_message , tmp_keyboard)

def random_string ():
    from string import ascii_letters
    from random import choice
    return ''.join(choice(ascii_letters) for i in range(10))

def main_page (karbar):
    my_bot = defs(values.bot_token())
    user_id = karbar.ID
    main_page_keyboard_init = values.main_page_keyboard_init()

    tmp_message = 'سلام %s \n عزیز لطفا بین گزینه ها انتخاب کن تا من جواب بدم' % karbar.name
    my_bot.send_message(user_id , tmp_message , main_page_keyboard_init())

    for message in my_bot.get_message():
        if message['from'] == user_id:
            if message['type'] == 'TEXT':
                txt = message['body']
                if txt == '//start_game_main_page':
                    my_bot.start_game(karbar)
                if txt == '//change_name_main_page':
                    my_bot.change_name(karbar)
                    karbar.update_values()
                if txt == '//amtiaz_ha_main_page':
                    my_bot.amtiaz_hai_karbar(karbar)
                if txt == '//delete_data_main_page':
                    my_bot.reset_rank(karbar)
                    karbar = user(user_id)
                if txt == '//best_gamer_main_page':
                    my_bot.show_best_gamer(karbar)
                if txt == '//help_about_game':
                    my_bot.help_about_game(karbar)
            else:
                my_bot.send_message(user_id , 'متاسفم لطفا فقط از حروف استفاده کنید و یا از کیبورد کمک بگیرید')

def game_loop (karbar):
    me_token = values.me_token()
    my_bot = defs(values.bot_token())
    karbar = user(me_token)
    keyboard_game_init = values.game_loop_keyboard_init()
    user_id = karbar.ID
    SQL = values.sql_connect()
    cursor = SQL.cursor()
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

    cursor.execute('SELECT ID FROM %s' % server_loc)
    users_id_server = cursor.fetchall()
    for har_user in users_id_server:
        my_bot.send_message(har_user[0] , 'کاراکتر شما هست: %s' % x[countertmp])
        dict_user_karakter[karakters[countertmp]] = har_user
        countertmp += 1

    # خود بازی
    my_bot.change_keyboard(user_id , keyboard_game_init)
    for message in my_bot.get_message():
        my_bot.change_keyboard(user_id , keyboard_game_init)
        print (message)
        if message['from'] == user_id:
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
                    my_bot.daraiy_ha_game(user_id , server_loc)
                my_bot.change_keyboard(user_id , keyboard_game_init)
            else:
                my_bot.send_group(server_loc , karbar.name , message['body'])
                my_bot.change_keyboard(user_id , keyboard_game_init)
