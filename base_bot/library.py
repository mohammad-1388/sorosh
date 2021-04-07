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
                SQL.commit()
                cursor.execute('SELECT * FROM Users WHERE ID="%s"' % user_id)
                t = 'حالا دیگه عضو بازی شدی می تونی وارد بازی بشی و بقیه رو دعوت کنی تا سکه بگیری \nراستی ۲۰ تا سکه هم برای عضو شدنت به حسابت اضافه شد'
                bot.send_message(user_id , t)
                return cursor.fetchall()[0]

            if not body[0:2] == '//':
                name_karbar = body
                tmp_message = 'اسم شما %s هست دیگه نه؟' % name_karbar

            if body == '//no_create_user': # wrong onderstand
                bot.send_message(user_id , 'ببخشید لطفا دوباره بگید')
                name_karbar = None
            if name_karbar != None:
                bot.send_message(user_id , tmp_message , tmp_keyboard)

def writer (text , loc , back_salsh=True , mode='a'):
    with open(loc , mode) as File:
        File.write(text)
        if back_salsh:
            File.write('\n')
        File.close()

def writer_DB (table , w_values , values_r , DB=values.sql_connect()):
    cursor = DB.cursor()
    if type(values_r) == type('a'):
        values_r = tuple([values_r])
    if type(w_values) == type('a'):
        w_values = tuple([w_values])

def cards_info (card_code):
    SQL = values.sql_connect()
    cursor = SQL.cursor()
    cursor.execute('SELECT * FROM card_info WHERE card_id="%s"' % card_code)
    
