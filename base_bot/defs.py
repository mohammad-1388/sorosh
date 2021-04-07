from client import Client
import values
from library import *
import code
SQL = values.sql_connect()
cursor = SQL.cursor()

class defs:

    def __init__ (self , bot_token):
        self.bot_token = bot_token
        self.client = Client(bot_token)

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

    def send_group (self , loc , name_karbar , message , keyboard=None):
        text = '%s : %s'
        cursor.execute('SELECT ID FROM %s' % (loc))
        group = cursor.fetchall()
        for har_fard in group:
            self.send_message(har_fard[0] , text % (name_karbar , message) , keyboard)

    def magics_game (self , user_id):
        pass

    def daraiy_ha_game (self , user_id , server , arsal:bool=True):
        data = server

        tmp_lambda = lambda a : len(a) if a != None else 0
        tmp_lambda_2 = lambda a : a if a != None else 'هیچی'

        if data.karakter_one == None or data.karakter_two == None:
            tmp_message = 'کارت های شما: %s\nتعداد کارت ها: %i\nکارت های ساخته شده شما: %s\nتعداد ساختمان های ساخته شده: %i\nتعداد سکه ها: %i\n' % (tmp_lambda_2(data.cards) , tmp_lambda(data.cards) , tmp_lambda_2(data.create_cards) , tmp_lambda(data.create_cards) , data.coins)

        else:
            tmp_message = 'کارت های شما: %s\nتعداد کارت ها: %i\nکارت های ساخته شده شما: %s\nتعداد ساختمان های ساخته شده: %i\nتعداد سکه ها: %i\nکاراکتر شما هست: %s' % (data.cards , tmp_lambda(data.cards) , data.create_cards , tmp_lambda(data.create_cards) , data.coins , data.karakter_one + ',' +data.karakter_two)

        if arsal:
            self.send_message(user_id , tmp_message)
        else:
            return [data.cards , tmp_lambda(data.cards) , data.create_cards , tmp_lambda(data.create_cards) , data.coins]

    def exit_game (self , user_id , loc):
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
        for message in self.get_message():
            if message['body'][0:2] == '//':
                if message['body'] == '//yes_reset_rank':
                    cursor.execute('DELETE FROM Users WHERE ID="%s"' % user_id)
                    SQL.commit()
                    self.send_message(user_id , 'اطلاعات شما با موفقیت پاک شد')
                    return True
                if message['body'] == '//no_reset_rank':
                    self.send_message(user_id , 'باشه')
                    return False
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
                    code.game_loop(karbar)
                if body == '//no_start_game_main_page':
                    self.send_message(karbar.ID , 'باشه')
                    break

    def change_name (self , karbar):
        user_id = karbar.ID
        name_karbar = None
        tmp_message_2 = 'لطفا اسم خود را وارد نمایید'
        tmp_keyboard_2 = [ [{'text' : 'منصرف شدم' , 'command' : '//cancel_change_name_main_page'}] ]
        self.send_message(user_id , tmp_message_2 , tmp_keyboard_2)

        for message in self.get_message():

            if message['from'] == user_id:
                body = message['body']
                if message['body'] == '//cancel_change_name_main_page': # cancel
                    self.send_message(user_id , 'باشه')
                    return False
                if body == '//yes_change_name': # change name
                    karbar.updater('Name' , name_karbar)
                    self.send_message(user_id , 'اسم شما با موفقیت تغییر کرد')
                    return True
                if not body[0:2] == '//':
                    name_karbar = body
                if body == '//no_change_name': # wrong onderstand
                    self.send_message(user_id , 'ببخشید لطفا دوباره بگید')
                    name_karbar = None
                if name_karbar != None:
                    tmp_message = 'اسم شما %s هست دیگه نه؟' % name_karbar
                    tmp_keyboard = [[{'text' : 'اره همینه' , 'command' : '//yes_change_name'} , {'text' : 'نه اشتباهه' , 'command' : '//no_change_name'}]]
                    self.send_message(user_id , tmp_message , tmp_keyboard)

    def amtiaz_hai_karbar (self , karbar):
        cursor.execute('SELECT Amtiaz , TDavat , TCoin FROM Users WHERE ID="%s"' % karbar.ID)
        data = cursor.fetchall()[0]
        tmp = 'امتیاز شما هست: %i\nتعداد نفرات دعوت شده توسط شما هست: %i\nنعداد سکه های شما هست: %i' % (data[0] , data[1] , data[2])
        self.send_message(karbar.ID , tmp)

    def show_best_gamer (self , karbar , keyboard=None):
        list_name = ['بهترین های این بازی از لحاظ امتیاز برابر است با:\n']
        tmp = ' %s : %s'
        counter = 0
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('SELECT Amtiaz , Name FROM Users')
        data = cursor.fetchall()
        data.sort(reverse=True)

        for har_shakhs in data:
            number = jaigozari(har_shakhs[0])

            if counter == 11:
                break
            if counter == 0:
                list_name.append('🥇.' + tmp % (har_shakhs[1] , number))
            elif counter == 1:
                list_name.append('🥈.' + tmp % (har_shakhs[1] , number))
            elif counter == 2:
                list_name.append('🥉.' + tmp % (har_shakhs[1] , number))
            else:
                list_name.append('🌟.' + tmp % (har_shakhs[1] , number))
            counter += 1
        list_name.append('\n\n⭕️' + tmp % (karbar.name , karbar.amtiaz))

        self.send_message(karbar.ID , '\n'.join(list_name) , keyboard)

    def help_about_game (self , karbar , keyboard=None):
        pass
