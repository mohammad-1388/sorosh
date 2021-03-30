from values import sql_connect
from library import random_string
from os import chdir

chdir('base_bot/')
SQL = sql_connect()

def writer (text , loc , back_salsh=True , mode='a'):
    with open(loc , mode) as File:
        File.write(text)
        if back_salsh:
            File.write('\n')
        File.close()

def writer_DB (table:str , w_values:tuple , values:tuple , DB=sql_connect()):
    cursor = DB.cursor()
    if type(values) == type('a'):
        values = tuple([values])
    if type(w_values) == type('a'):
        w_values = tuple([w_values])

    cursor.execute('INSERT INTO %s (%s) VALUES (%s)' % (table , ','.join(w_values) , '\"' + '\",\"'.join(values) +'\"'))
    DB.commit()
    DB.close()

def create_room ():
    rand = random_string()
    cursor = SQL.cursor()
    cursor.execute('CREATE TABLE %s (counter_users int(1) AUTO_INCREMENT KEY , ID varchar(60) , cards int(2) DEFAULT 0, create_card int(1) DEFAULT 0, coins int(2) DEFAULT 2, karakter varchar(10) , karaktertwo varchar(10) DEFAULT "None")' % rand)
    SQL.commit()
    writer(rand , 'server_list.txt')
    return rand

def find_room (user_id):
    cursor = SQL.cursor()
    sang = True

    with open('server_list.txt' , 'r') as list_server:
        list_server = list_server.readlines()
    for har_server in list_server:
        har_server = har_server.strip('\n')
        cursor.execute('SELECT counter_users FROM %s' % har_server)
        last = cursor.fetchall()
        if last == []:
            continue
        if last.pop()[0] <= 6:
            writer_DB(har_server , 'ID' , user_id)
            return har_server
    if sang:
        tmp = create_room()
        writer_DB(tmp , 'ID' , user_id)
        return tmp

def delete_room (Name):
    cursor = SQL.cursor()
    cursor.execute('DROP TABLE %s' % Name)
    SQL.commit()
    SQL.close()

    with open ('server_list.txt' , 'r+') as server_list:
        lines = server_list.readlines()
        server_list.close()
    with open ('server_list.txt' , 'w') as server_list:
        for line in lines:
            if line.strip() != Name:
                server_list.write(line)
