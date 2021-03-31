import mysql.connector
from defs import defs
import values
from library import *

class user:
    def __init__ (self , user_id):
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('SELECT * FROM Users WHERE ID="%s"' % user_id)
        cursor = cursor.fetchall()
        if cursor == []:
            cursor = create_user(user_id)
        else:
            cursor = cursor[0]

        self.ID = cursor[0]
        self.name = cursor[1]
        self.amtiaz = cursor[2]
        self.uadmin = cursor[3]
        self.tdavat = cursor[4]
        self.tcoin = cursor[5]

    def updater (self , block , new):
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('UPDATE Users SET %s=%s WHERE ID=%s' % (block , '\"'+new+'\"' , '\"'+self.ID+'\"'))
        SQL.commit()
        SQL.close()

    def update_values (self):
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('SELECT * FROM Users WHERE ID="%s"' % self.ID)
        cursor = cursor.fetchall()
        cursor = cursor[0]

        self.ID = cursor[0]
        self.name = cursor[1]
        self.amtiaz = cursor[2]
        self.uadmin = cursor[3]
        self.tdavat = cursor[4]
        self.tcoin = cursor[5]
