from defs import defs
import values

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
    user_id = karbar.ID
    