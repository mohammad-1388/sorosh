import mysql.connector
from defs import defs
import values
from library import create_user

SQL = values.sql_connect()
cursor = SQL.cursor()

class user:
    def __init__ (self , user_id):
        cursor = SQL.cursor()
        cursor = cursor.execute('SELECT * FROM Users WHERE ID="%s"' % user_id)
        if cursor == None:
            cursor = create_user(user_id)
        for ID , name , amtiaz , uadmin , tdavat , tcoin in cursor:
            self.ID = ID
            self.name = name
            self.amtiaz = amtiaz
            self.uadmin = uadmin
            self.tdavat = tdavat
            self.tcoin = tcoin

    def updater (self , block , new , last_or_user_id):
        cursor = SQL.cursor()
        cursor.execute('UPDATE Users SET %s=%s WHERE %s=%s' % block , new , block , last_or_user_id)


Erfan = user(values.me_token())
print (Erfan)