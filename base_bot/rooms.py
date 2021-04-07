import values
import library

SQL = values.sql_connect()

class room:

    def __init__ (self , karbar):
        user_id = karbar.ID
        cursor = SQL.cursor()
        sang = True

        # find server#
        with open('server_list.txt' , 'r') as list_server:
            list_server = list_server.readlines()
        for har_server in list_server:
            har_server = har_server.strip('\n')
            cursor.execute('SELECT counter_users FROM %s' % har_server)
            last = cursor.fetchall()
            if last == []:
                continue
            if last.pop()[0] <= 6:
                library.writer_DB(har_server , 'ID' , user_id)
                self.server_loc = har_server
                sang = False

        if sang:
            tmp = self.create_room()
            library.writer_DB(tmp , 'ID' , user_id)
            self.server_loc = tmp
        #            #

        self.user_id = user_id
        cursor = SQL.cursor()
        cursor.execute('INSERT INTO %s (ID) VALUES ("%s")' % (self.server_loc , user_id))
        SQL.commit()
        cursor.execute('SELECT * FROM %s WHERE ID="%s"' % (self.server_loc , user_id))
        data = cursor.fetchall()[0]

        self.number = data[0]
        self.cards = data[2]
        self.create_cards = data[3]
        self.coins = data[4]
        self.karakter_one = data[5]
        self.karakter_two = data[6]

    def create_room (self): # counter , (ID) , (cards) , create_cards , coins , karakters , karaktertwo
        rand = library.random_string()
        cursor = SQL.cursor()
        cursor.execute('CREATE TABLE %s (counter_users int(1) AUTO_INCREMENT KEY , ID varchar(60) , cards varchar(200) , create_cards varchar(200), coins int(2) DEFAULT 2 , karakter varchar(10) , karaktertwo varchar(10) )' % rand)
        SQL.commit()
        library.writer(rand , 'server_list.txt')
        return rand

    def delete_room (self):
        Name = self.server_loc
        cursor = SQL.cursor()
        cursor.execute('DROP TABLE %s' % Name)
        SQL.commit()

        with open ('server_list.txt' , 'r+') as server_list:
            lines = server_list.readlines()
            server_list.close()
        with open ('server_list.txt' , 'w') as server_list:
            for line in lines:
                if line.strip() != Name:
                    server_list.write(line)

    def updater (self , column:str , value):
        cursor = SQL.cursor()

        if column == 'cards' or column == 'create_cards':
            value = ','.join(value)
        if type(value) == type(10):
            cursor.execute('UPDATE Users SET %s=%s WHERE ID="%s"' % (column , value , self.user_id))
        else:
            cursor.execute('UPDATE Users SET %s="%s" WHERE ID="%s"' % (column , value , self.user_id))
        self.update_values()

    def update_values (self):
        cursor = SQL.cursor()
        cursor.execute('SELECT * FROM %s WHERE ID="%s"' % (self.server_loc , self.user_id))
        data = cursor.fetchall()[0]

        self.number = data[0]
        self.cards = data[2].split(',')
        self.create_cards = data[3].split(',')
        self.coins = data[4]
        self.karakter_one = data[5]
        self.karakter_two = data[6]
