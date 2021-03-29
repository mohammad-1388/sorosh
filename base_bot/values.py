from mysql.connector import connect

def bot_token ():
    return 'EW4Ym48lRJUqm7v4gGmapwJs7GSztlNCRprRc83izDSBgUTa6AlrZoM9VoIe3loVAFRMkA7HDkSyBWeCNzUkxNAFmPbI5j8tu6drR2k-NX_NpKFfw-bozOd3JB3MeH878acwf8mzEAdkXHIG'

def me_token ():
    return 'lbPaUy7i3eV9N9MQc15gEul_34Nas6ye0wRqIYPT3-U1fRCiFtEwvqK9ouA'

def game_loop_keyboard():
    return [ [{'text' : 'دارایی ها' , 'command' : '//daraiy_ha'} , {'text' : 'چت خصوصی' , 'command' : '//privet_chat'}] , 
                       [{'text' : 'جادو ها'   , 'command' : '//magics'   } , {'text' : 'خروج از بازی' , 'command' : '//exit_game'}] ]

def sql_connect ():
    return connect(user='Erfan' , password='nohack' , database='mybot')