import mysql.connector


class Connection:

    cnx = mysql.connector.connect(user='sql7234823', password='WEhqj9sjiX',
                                  host='sql7.freemysqlhosting.net',
                                  database='sql7234823')
    cursor = cnx.cursor()
    IntegrityError = mysql.connector.IntegrityError

    def getcursor(self):
        return self.cursor

    def getcnx(self):
        return self.cnx
