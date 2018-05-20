from masterDAO import Connection

connection = Connection()


class LeaderboardDAO:

    @staticmethod
    def show_leader():
        try:
            db = connection.getcursor()
            sql = 'SELECT username, cash, totalcurrent FROM users ORDER BY totalcurrent DESC'
            db.execute(sql)
            return db.fetchall()
        finally:
            pass
