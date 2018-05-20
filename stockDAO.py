from masterDAO import Connection
import datetime

connection = Connection()


class StockDAO:

    @staticmethod
    def stock_info(stock):
        """
        INPUT: stock
        RETURN: All data from the corresponding row in the database
        """
        db = connection.getcursor()
        try:
            sql = "SELECT a.stockID, b.currency, a.name, a.price  FROM stocks a JOIN currencies b " \
                  "ON a.currencyID = b.currencyID " \
                  "WHERE a.symbol=%s"
            db.execute(sql, [stock.symbol])
            info = db.fetchone()
            return info
        finally:
            pass

    @staticmethod
    def stock_info_all():
        """
        RETURN: Info about all stocks
        """
        db = connection.getcursor()
        try:
            sql = "SELECT * FROM stocks"
            db.execute(sql)
            info = db.fetchall()
            return info
        finally:
            pass

    @staticmethod
    def check_stock(stock):
        """
        INPUT: stock
        Check if there is an entry for this stock.
        RETURN: - True
                - False
        """
        try:
            db = connection.getcursor()
            sql = "SELECT EXISTS(SELECT * FROM stocks WHERE symbol=%s)"
            db.execute(sql, [stock.symbol])
            if db.fetchone()[0]:
                return True
            else:
                return False
        finally:
            pass

    @staticmethod
    def new_stock(stock):
        """
        INPUT: stock
        Save all information available from the API to the stock table.
        Output: True/False
        """
        try:
            db = connection.getcursor()
            sql = "INSERT INTO stocks (currencyID, symbol, name, price, date) " \
                  "VALUES " \
                  "((SELECT currencyID FROM currencies WHERE currency = %s), " \
                  "%s, %s, %s, %s)"
            db.execute(sql, [stock.currency, stock.symbol, stock.name, stock.price, datetime.datetime.now()])
            return True
        except connection.IntegrityError:
            return "Invalid currency"
        finally:
            connection.getcnx().commit()

    @staticmethod
    def update_stock_prices(prices, symbols):
        """
        INPUT: stock
        Update stock price
        Output: True
        """
        try:
            db = connection.getcursor()
            for i in range(0, len(prices)):
                sql = "UPDATE stocks SET price=(%s), date=(%s) WHERE symbol=(%s)"
                db.execute(sql, [prices[i], datetime.datetime.now(), symbols[i]])
        finally:
            connection.getcnx().commit()

    @staticmethod
    def get_symbols(user):
        db = connection.getcursor()
        try:
            sql = "SELECT b.symbol " \
                  "FROM " \
                  "  (SELECT stocks_stockID FROM portfolio WHERE users_userID=%s)" \
                  " AS a " \
                  "JOIN " \
                  "  (SELECT symbol , stockID FROM stocks) " \
                  " AS b " \
                  "ON a.stocks_stockID=b.stockID;"
            db.execute(sql, [user.ID])
            return db.fetchall()
        finally:
            pass

    @staticmethod
    def getdate():
        db = connection.getcursor()
        try:
            sql = "SELECT * FROM stocks limit 1"
            db.execute(sql)
            return db.fetchone()[5]
        finally:
            pass
