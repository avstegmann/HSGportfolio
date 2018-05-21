from masterDAO import Connection
import datetime

connection = Connection()
db = connection.getcursor()


class PortfolioDAO:

    @staticmethod
    def check(stock, user):
        try:
            sql = "SELECT EXISTS(SELECT * FROM portfolio WHERE users_userID=%s and stocks_stockID=%s)"
            db.execute(sql, [user.ID, stock.ID])
            return db.fetchone()[0]
        finally:
            pass

    @staticmethod
    def get_rows():
        try:
            sql = "SELECT COUNT(*) FROM portfolio"
            db.execute(sql)
            return db.fetchone()[0]
        finally:
            pass

    @staticmethod
    def get_info(user):
        try:
            sql = "SELECT portfolio.name, portfolio.shares, portfolio.buyingprice, info.currency, " \
                  "portfolio.exchange_rate, portfolio.expenses, portfolio.cprice, portfolio.cvalue " \
                  "FROM " \
                  "   ((SELECT a.name, b.shares, b.buyingprice, a.currencyID, b.exchange_rate, b.expenses, " \
                  "    a.price as cprice, (b.shares*a.price) as cvalue, a.symbol " \
                  "    FROM stocks a JOIN portfolio b on a.stockID = b.stocks_stockID " \
                  "    WHERE users_userID=(SELECT userID FROM users WHERE username=%s) " \
                  "    ORDER BY a.name DESC) " \
                  "   AS portfolio " \
                  "  JOIN" \
                  "  (SELECT a.currency, b.symbol" \
                  "   FROM currencies a JOIN stocks b on a.currencyID = b.currencyID)" \
                  "   AS info " \
                  "  ON portfolio.symbol = info.symbol) " \
                  "ORDER BY portfolio.name ASC"
            db.execute(sql, [user.username])
            info = db.fetchall()
            print(info)
            return info
        finally:
            pass

    @staticmethod
    def update_user_cash_buy(user, expenses, rate):
        try:
            # Update user's cash
            sql = "UPDATE users SET cash=%s WHERE userID=%s"
            db.execute(sql, [user.cash - float(expenses)*float(rate), user.ID])
        finally:
            connection.getcnx().commit()

    @staticmethod
    def update_user_cash_sell(user, earnings, rate):
        try:
            # Update user's cash
            sql = "UPDATE users SET cash=%s WHERE userID=%s"
            db.execute(sql, [user.cash + float(earnings) * float(rate), user.ID])
        finally:
            connection.getcnx().commit()

    def buy_merge(self, user, stock, shares, pair, rate):
        date = datetime.datetime.now()
        # Update stock in user's porfolio
        try:
            sql = "SELECT buyingprice, expenses, shares FROM portfolio " \
                  "WHERE users_userID=%s and stocks_stockID=%s; "
            db.execute(sql, [user.ID, stock.ID])
            fetch = db.fetchone()
            buyingprice = fetch[0]
            expenses2 = fetch[1]
            shares2 = fetch[2]
        finally:
            pass
        avg = (buyingprice + stock.price)/2
        expenses = float(shares) * float(stock.price)
        expenses_new = (expenses + expenses2) / 2
        shares_new = shares + shares2
        try:
            sql = "UPDATE portfolio SET shares=%s, buyingprice=%s, expenses=%s, " \
                  "exchange_rate=(SELECT rate FROM exchange_rates WHERE pair=%s), date=%s " \
                  "WHERE users_userID=%s and stocks_stockID=%s"
            db.execute(sql, [shares_new, avg, expenses_new, pair, date, user.ID, stock.ID])
        finally:
            pass
        try:
            sql = "INSERT INTO history " \
                  "(historyID, users_userID, stock_stockID, shares, buyingprice, value, exchange_rate)" \
                  "VALUES" \
                  "(%s, %s, %s, %s, %s, %s, (SELECT rate FROM exchange_rates WHERE pair=%s))"
            db.execute(sql, [date, user.ID, stock.ID, shares, stock.price, (-1) * expenses, pair])
        finally:
            connection.getcnx().commit()
        self.update_user_cash_buy(user, expenses, rate)

    def buy_new(self, user, stock, shares, pair, rate):
        expenses = float(shares) * float(stock.price)
        date = datetime.datetime.now()
        # Add stock to user's porfolio
        try:
            sql = "INSERT INTO portfolio " \
                  "(users_userID, stocks_stockID, shares, buyingprice, expenses, exchange_rate, date) " \
                  "VALUES " \
                  "(%s, %s, %s, %s, %s, (SELECT rate FROM exchange_rates WHERE pair=%s), %s)"
            db.execute(sql, [user.ID, stock.ID, shares, stock.price, expenses, pair, date])
        finally:
            pass
        try:
            sql = "INSERT INTO history " \
                  "(historyID, users_userID, stock_stockID, shares, buyingprice, value, exchange_rate)" \
                  "VALUES" \
                  "(%s, %s, %s, %s, %s, %s, (SELECT rate FROM exchange_rates WHERE pair=%s))"
            db.execute(sql, [date, user.ID, stock.ID, shares, stock.price, (-1)*expenses, pair])
        finally:
            connection.getcnx().commit()
        self.update_user_cash_buy(user, expenses, rate)

    def sell_all(self, user, stock, shares, pair, rate):
        earnings = shares * stock.price
        date = datetime.datetime.now()
        # Delete stock from user's porfolio
        try:
            sql = "DELETE FROM portfolio WHERE users_userID=%s and stocks_stockID=%s and shares=%s LIMIT 1"
            db.execute(sql, [user.ID, stock.ID, shares])
        finally:
            pass
        try:
            sql = "INSERT INTO history " \
                  "(historyID, users_userID, stock_stockID, shares, buyingprice, value, exchange_rate)" \
                  "VALUES" \
                  "(%s, %s, %s, %s, %s, %s, (SELECT rate FROM exchange_rates WHERE pair=%s))"
            db.execute(sql, [date, user.ID, stock.ID, shares, stock.price, earnings, pair])
        finally:
            connection.getcnx().commit()
        self.update_user_cash_sell(user, earnings, rate)

    def sell_part(self, user, stock, shares_sold, shares_left, pair, rate):
        earnings = shares_sold * stock.price
        date = datetime.datetime.now()
        try:
            sql = "SELECT buyingprice, date FROM portfolio " \
                  "WHERE users_userID=%s and stocks_stockID=%s " \
                  "ORDER BY date ASC LIMIT 1"
            db.execute(sql, [user.ID, stock.ID])
            fetch = db.fetchone()
            buyingprice = fetch[0]
            orig_date = fetch[1]
        finally:
            pass
        remaining_expenses = shares_left * buyingprice
        # Update stock entry in user's porfolio
        try:
            sql = "UPDATE portfolio SET shares=%s, expenses=%s " \
                  "WHERE users_userID=%s and stocks_stockID=%s and date=%s"
            db.execute(sql, [shares_left, remaining_expenses, user.ID, stock.ID, orig_date])
        finally:
            pass
        try:
            sql = "INSERT INTO history " \
                  "(historyID, users_userID, stock_stockID, shares, buyingprice, value, exchange_rate)" \
                  "VALUES" \
                  "(%s, %s, %s, %s, %s, %s, (SELECT rate FROM exchange_rates WHERE pair=%s))"
            db.execute(sql, [date, user.ID, stock.ID, shares_sold, stock.price, earnings, pair])
        finally:
            connection.getcnx().commit()
        self.update_user_cash_sell(user, earnings, rate)

    @staticmethod
    def get_shares(user, stock):
        try:
            sql = "SELECT shares FROM portfolio " \
                  "WHERE users_userID=%s and stocks_stockID=%s " \
                  "ORDER BY date ASC LIMIT 1"
            db.execute(sql, [user.ID, stock.ID])
            return db.fetchone()[0]
        finally:
            pass

    @staticmethod
    def get_history(user):
        try:
            sql = "SELECT history.historyID, history.name, history.shares, history.buyingprice, info.currency, " \
                  "history.value, history.exchange_rate " \
                  "FROM " \
                  "((SELECT a.historyID, b.name, a.shares, a.buyingprice, a.value, a.exchange_rate, b.symbol " \
                  "   FROM history a JOIN stocks b " \
                  "   ON a.stock_stockID=b.stockID " \
                  "   WHERE a.users_userID=%s " \
                  "   ORDER BY a.historyID DESC) " \
                  "  AS history " \
                  "JOIN" \
                  "(SELECT a.currency, b.symbol" \
                  "   FROM currencies a JOIN stocks b on a.currencyID = b.currencyID)" \
                  "   AS info " \
                  "ON history.symbol = info.symbol) " \
                  "ORDER BY history.historyID DESC"
            db.execute(sql, [user.ID])
            return db.fetchall()
        finally:
            pass

    @staticmethod
    def get_exchange_rates():
        try:
            sql = "SELECT * FROM exchange_rates"
            db.execute(sql)
            return db.fetchall()
        finally:
            pass

    @staticmethod
    def update_exchange_rate(pair, rate):
        try:
            sql = "UPDATE exchange_rates SET rate=%s, date=%s " \
                  "WHERE pair=%s"
            db.execute(sql, [rate, datetime.datetime.now(), pair])
            return db.fetchone()
        finally:
            connection.getcnx().commit()
