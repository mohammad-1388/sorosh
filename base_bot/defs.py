from os import chdir
from client import Client
import values
from library import *

class defs:
    def __init__ (self , bot_token):
        self.bot_token = bot_token
        self.client = Client(bot_token)
        SQL = values.sql_connect()

    def get_message (self):
        messages = self.client.get_messages()
        for message in messages:
            yield message
    
    def send_message (self , to , message , keyboard=None):
        self.client.send_text(to, message , self.client.make_keyboard(keyboard))

    def change_keyboard (self , to , keyboard):
        self.client.change_keyboard(to, self.client.make_keyboard(keyboard))

    def random_karakter (self , list_karakters=['ادمکش' , 'راهزن' , 'تردست' , 'شاه' , 'حکیم' , 'تاجر' , 'معمار' , 'سردار'] , sample_n=1):
        from random import sample
        return sample(list_karakters , sample_n)

    def send_group (self , loc , name_karbar , message):

        text = '%s : %s'
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('SELECT ID FROM %s' % (loc))
        group = cursor.fetchall()
        for har_fard in group:
            self.send_message(har_fard[0] , text % (name_karbar , message))
        SQL.close()

    def magics_game (self , user_id):
        pass

    def daraiy_ha_game (self , user_id , server_name , arsal:bool=True):
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('SELECT cards , create_card , coins , karakter , karaktertwo FROM %s WHERE ID="%s"' % ('WiNgStGMbn' , values.me_token()))
        x = cursor.fetchall()
        x = x[0]
        SQL.close()

        tmp_message = 'کاراکتر دوم شما هست: %s' % (x[4])
        tmp_lambda = lambda x : tmp_message if x == 'None' else ''
        tmp_message_2 = '''تعداد کارت ها: %i
        تعداد ساختمان های ساخته شده: %i
        تعداد سکه ها: %i
        کاراکتر شما هست: %s
        %s''' % (x[0] , x[1] , x[2] , x[3] , tmp_lambda(x[4]))

        if arsal:
            self.send_message(user_id , tmp_message_2)
        else:
            return tmp_message_2

    def exit_game (self , user_id , loc):
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        tmp_keyboard = [[{'text' : 'بله' , 'command' : '//yes_exit'} , {'text' : 'نه' , 'command' : '//no_exit'}]]
        self.send_message(user_id , 'ایا مطمعن به خروج از بازی هستید؟' , tmp_keyboard)
        for message in self.get_message():
            if message['body'][0:2] == '//':
                if message['body'] == '//yes_exit':
                    cursor.execute('DELETE FROM %s WHERE ID="%s"' % (loc , user_id))
                    return True

                if message['body'] == '//no_exit':
                    self.send_message(user_id , 'باشه پس به بازی ادامه بده' , values.game_loop_keyboard_init())
                    return False
            else:
                self.send_group(loc , user_id , message['body'])

    def reset_rank (self , user_id):
        tmp_message = 'ایا مطمعن به پاک کردن تمام اطلاعات خود شامل امتیاز , نام و  id شما در ربات هستید؟'
        tmp_keyboard = [[{'text' : 'بله' , 'command' : '//yes_reset_rank'} , {'text' : 'نه' , 'command' : '//no_reset_rank'}]]
        self.send_message(user_id , tmp_message , tmp_keyboard)
        cursor = SQL.cursor()
        for message in self.get_message():
            if message['body'][0:2] == '//':
                if message['body'] == '//yes_reset_rank':
                    cursor.execute('DELETE FROM Users WHERE ID="%s"' % user_id)
                    SQL.commit()
                    self.send_message(user_id , 'اطلاعات شما با موفقیت پاک شد')
                    break
                if message['body'] == '//no_reset_rank':
                    self.send_message(user_id , 'باشه')
                    break
            else:
                self.send_message(user_id , 'جوون؟ :/')

    def start_game (self , karbar):
        tmp_message = 'ایا مطمعن به شروع بازی هستید؟'
        tmp_keyboard = [ [{'text' : 'بله' , 'command' : '//yes_start_game_main_page'} , {'text' : 'نه' , 'command' : '//no_start_game_main_page'}] ]
        self.send_message(karbar.ID , tmp_message , tmp_keyboard)

        for message in self.get_message():
            if message['from'] == karbar.ID:
                body = message['body']
                if body == '//yes_start_game_main_page':
                    game_loop(karbar)
                if body == '//no_start_game_main_page':
                    self.send_message(karbar.ID , 'باشه')
                    break
                else:
                    self.send_message(karbar.ID , 'جون؟ :/')

    def change_name (self , karbar):
        user_id = karbar.ID
        tmp_message = 'لطفا اسم خود را وارد نمایید'
        tmp_keyboard = [ [{'text' : 'منصرف شدم' , 'command' : '//cancel_change_name_main_page'}] ]
        self.send_message(user_id , tmp_message , tmp_keyboard)

        for message in bot.get_message():
            if message['from'] == user_id:
                body = message['body']
                if message['body'] == '//cancel_change_name_main_page':
                    self.send_message(user_id , 'باشه')
                    break
                if body == '//yes_change_name':
                    karbar.updater('Name' , name_karbar)

                name_karbar = message['body']
                tmp_message = 'اسم شما %s هست دیگه نه؟' % name_karbar
                tmp_keyboard = [[{'text' : 'اره همینه' , 'command' : '//yes_change_name'} , {'text' : 'نه اشتباهه' , 'command' : '//no_change_name'}]]

                self.send_message(user_id , tmp_message , tmp_keyboard)

    def amtiaz_hai_karbar (self , karbar):
        pass

    def show_best_gamer (self , karbar):
        pass

    def help_about_game (self , karbar):
        self.send_message(karbar.ID , values.messge_help_about_game())
