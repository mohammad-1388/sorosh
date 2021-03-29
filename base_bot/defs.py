from mysql.connector import connect
from os import chdir
from client import Client
import values
SQL = values.sql_connect()

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

    def send_group (self , loc , name_karbar , message):
        try:
            chdir('base_bot/server_tmp/')
        except:
            pass

        text = '%s : %s'
        with open(loc , 'r') as users:
            group = users.readlines()
            for har_fard in group:
                self.send_message(har_fard.strip() , text % (name_karbar , message))

            users.close()

    def magics_game (self , user_id):
        pass

    def daraiy_ha_game (self , user_id):
        pass

    def exit_game (self , user_id , loc):
        tmp_keyboard = [[{'text' : 'بله' , 'command' : '//yes_exit'} , {'text' : 'نه' , 'command' : '//no_exit'}]]
        self.send_message(user_id , 'ایا مطمعن به خروج از بازی هستید؟' , tmp_keyboard)
        for message in self.get_message():
            if message['body'][0:2] == '//':
                if message['body'] == '//yes_exit':
                    #
                    try:
                        chdir('base_bot/server_tmp/')
                    except:
                        pass
                    with open (loc , 'r+') as server_user:
                        lines = server_user.readlines()
                        server_user.close()
                    with open (loc , 'w') as server_user:
                        for line in lines:
                            if line.strip() != user_id:
                                server_user.write(line)
                    return True
                    #
                if message['body'] == '//no_exit':
                    self.send_message(user_id , 'باشه پس به بازی ادامه بده' , values.game_loop_keyboard())
                    return False
            else:
                self.send_group(loc , user_id , message['body'])

    def reset_rank (self , user_id):
        tmp_message = 'ایا مطمعن به پاک کردن تمام اطلاعات خود شامل امتیاز , نام و  id شما در ربات هستید؟'
        tmp_keyboard = [[{'text' : 'بله' , 'command' : '//yes_reset_rank'} , {'text' : 'نه' , 'command' : '//no_reset_rank'}]]
        self.send_message(user_id , tmp_message , tmp_keyboard)
        cursor = SQL.cursor()
        for message in self.get_message():
            print (message)
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

