import values

class card_info:

    def __init__ (self , card_id):
        SQL = values.sql_connect()
        cursor = SQL.cursor()
        cursor.execute('SELECT * FROM cards_info WHERE card_id="%s"' % card_id)

        data = cursor.fetchall()[0]
        self.card_id = data[0]
        self.card_name = data[1]
        self.owner = data[2]
        self.buy = data[3]
        self.plus = data[4]
