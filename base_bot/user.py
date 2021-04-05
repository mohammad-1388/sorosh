import values
from library import *


class user:

    def __init__ (self , user_id):
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('SELECT * FROM Users WHERE ID="%s"' % user_id)
        data = cursor.fetchall()
        if data == []:
            data = create_user(user_id)
        else:
            data = data[0]

        self.ID = data[0]
        self.name = data[1]
        self.amtiaz = data[2]
        self.uadmin = data[3]
        self.tdavat = data[4]
        self.tcoin = data[5]

    def updater (self , block , new):
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('UPDATE Users SET %s=%s WHERE ID=%s' % (block , '\"'+new+'\"' , '\"'+self.ID+'\"'))
        SQL.commit()

    def update_values (self):
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('SELECT * FROM Users WHERE ID="%s"' % self.ID)
        data = cursor.fetchall()[0]

        self.ID = data[0]
        self.name = data[1]
        self.amtiaz = data[2]
        self.uadmin = data[3]
        self.tdavat = data[4]
        self.tcoin = data[5]
