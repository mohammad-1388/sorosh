def bot_token ():
    return 'EW4Ym48lRJUqm7v4gGmapwJs7GSztlNCRprRc83izDSBgUTa6AlrZoM9VoIe3loVAFRMkA7HDkSyBWeCNzUkxNAFmPbI5j8tu6drR2k-NX_NpKFfw-bozOd3JB3MeH878acwf8mzEAdkXHIG'

def me_token ():
    return 'lbPaUy7i3eV9N9MQc15gEul_34Nas6ye0wRqIYPT3-U1fRCiFtEwvqK9ouA'

def game_loop_keyboard_init():
    return [ [{'text' : 'دارایی ها' , 'command' : '//daraiy_ha'}] , [{'text' : 'جادو ها'   , 'command' : '//magics'   } , {'text' : 'خروج از بازی' , 'command' : '//exit_game'}] ]

def main_page_keyboard_init():
    return[ [{'text' : 'شروع بازی'       , 'command' : '//start_game_main_page'} , {'text' : 'تغییر نام'              , 'command' : '//change_name_main_page'}] ,
            [{'text' : 'امتیاز های من'   , 'command' : '//amtiaz_ha_main_page' } , {'text' : 'پاک کردن تمام امتیازات' , 'command' : '//delete_data_main_page'}] ,
            [{'text' : 'بهترین های بازی' , 'command' : '//best_gamer_main_page'} , {'text' : 'روش بازی'               , 'command' : '//help_about_game'      }] ]

def sql_connect ():
    from mysql.connector import connect
    return connect(user='Erfan' , password='nohack' , database='mybot')

def messge_help_about_game ():
    return ''''''