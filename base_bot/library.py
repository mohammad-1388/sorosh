import values

def random_string ():
    from string import ascii_letters
    from random import choice
    return ''.join(choice(ascii_letters) for i in range(10))

def jaigozari (vorodi):

    number = {
        '0' : '۰',
        '1' : '۱',
        '2' : '۲',
        '3' : '۳',
        '4' : '۴',
        '5' : '۵',
        '6' : '۶',
        '7' : '۷',
        '8' : '۸',
        '9' : '۹',
        '.' : ''}
    x = ''
    vorodi = str(vorodi)

    for har in vorodi:
        x = x + number[har]

    return x

def create_user(user_id):
    from defs import defs

    bot = defs(values.bot_token())
    SQL = values.sql_connect()
    cursor = SQL.cursor()
    name_karbar = None
    tmp_message = 'متاسفانه اسم شما در بازی ثبت نشده است لطفا اسم خود را وارد نمایید'
    tmp_keyboard = [[{'text' : 'اره همینه' , 'command' : '//yes_create_user'} , {'text' : 'نه اشتباهه' , 'command' : '//no_create_user'}]]
    bot.send_message(user_id , tmp_message)

    for message in bot.get_message():

        if message['from'] == user_id:

            body = message['body']
            if body == '//yes_create_user': # change name
                cursor.execute('INSERT INTO Users (ID , Name) VALUES ("%s" , "%s")' % (user_id , name_karbar))
                cursor.execute('SELECT * FROM Users WHERE ID="%s"' % user_id)
                t = 'حالا دیگه عضو بازی شدی می تونی وارد بازی بشی و بقیه رو دعوت کنی تا سکه بگیری \nراستی ۲۰ تا سکه هم برای عضو شدنت به حسابت اضافه شد'
                bot.send_message(user_id , '')
                return cursor.fetchall()[0]

            if not body[0:2] == '//':
                name_karbar = body
                tmp_message = 'اسم شما %s هست دیگه نه؟' % name_karbar

            if body == '//no_create_user': # wrong onderstand
                bot.send_message(user_id , 'ببخشید لطفا دوباره بگید')
                name_karbar = None
            if name_karbar != None:
                bot.send_message(user_id , tmp_message , tmp_keyboard)

def main_page (karbar):
    from user import user
    from defs import defs

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

def game_loop (karbar):
    from collections import OrderedDict
    from rooms import find_room
    from defs import defs

    dict_user_karakter = OrderedDict()
    me_token = values.me_token()
    my_bot = defs(values.bot_token())
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

    server_loc = find_room(user_id)

    # مرحله حذف شدن کاراکتر اول
    x = my_bot.random_karakter()
    my_bot.send_group(server_loc , 'سیستم' , 'کاراکتر %s حذف شد' % x[0])
    karakters.remove(x[0])

    # مرحله نتخاب کاراکتر شانسی
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
                my_bot.send_group(server_loc , karbar.name , message['body'] , keyboard_game_init)
