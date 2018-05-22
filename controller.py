from leaderboard import Leaderboard
from portfolio import Portfolio
from article import Article
from stock import Stock
from user import User
# import threading
import datetime
import json


class Controller:

    """
    # Open thread for background updates to the DB
    def __init__(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
    """

    user = User()
    stock = Stock()
    portfolio = Portfolio()
    leaderboard = Leaderboard()
    articles = {}

    def run(self):
        """
        Check if the DB has been updated this hour.
            - If not, update now
            - If so, update at the next full hour.
        """
        """
        # activate the code below, if the raspberry pi is not running
        now = datetime.datetime.now()
        date = self.stock.getdate()
        if (now - date).seconds // 3600 >= 1:
            self.update()
        """
        self.update()

    def update(self):
        """
        - Update the prices of all stocks
        - Update exchange rates
        """
        self.stock.update()
        usernames = self.user.get_usernames()
        for i in range(0, len(usernames)):
            self.user.username = usernames[i][0]
            self.user.init()
            self.portfolio.update_user(self.user)

    def login(self, username, password):
        """
        INPUT: controller, username, password
        Function checks whether user is registered and initializes missing data if he is.
        OUTPUT: True/False -> Feedback: username or password wrong. If true, object user is initialized.
        """
        self.user.username = username
        self.user.password = password
        check = self.user.login()

        return check

    def register(self, username, password):
        """
        INPUT: username, password
        Function checks if username is available. If so, it creates a new user with the
        given username, password.
        OUTPUT: True/False -> Feedback: username exists already
        """
        self.user.username = username
        self.user.password = password
        return self.user.new_user()

    def lookup(self, symbol):
        """
        INPUT stock symbol
        - get real time stock information from API  --->    initialize object stock
        - get real time news articles and           --->    initialize list of articles
                                                    --->    save articles in DB
        OUTPUT
        - True
        - False -> Invalid symbol or No news available.
        """
        symbol = symbol.upper()
        self.stock.symbol = symbol
        stockinfo = self.stock.lookup()
        if stockinfo is not True:
            return stockinfo

        article = Article()
        self.articles = article.lookup(self.stock, datetime.datetime.now().date())
        if self.articles is False:
            return "No news available."
        return True

    def buy(self, symbol, shares):
        """
        INPUT: stock symbol, desired # of shares
        - get real time stock information from API  --->    initialize object stock
        OUTPUT: - True (if purchase was successful)
                - False (+ error message)
        """
        symbol = symbol.upper()
        if symbol is "":
            return "Missing symbol"
        if shares is "":
            return "Missing shares"
        self.stock.symbol = symbol
        stockinfo = self.stock.lookup()
        if stockinfo is not True:
            return stockinfo
        purchase = self.portfolio.buy(self.user, self.stock, shares)
        return purchase

    def sell(self, symbol, shares):
        """
        INPUT: stock symbol, # of shares to sell
        - get real time stock information from API  --->    initialize object stock
        OUTPUT: - True (if purchase was successful)
                - False (+ error message)
        """
        symbol = symbol.upper()
        if symbol is "":
            return "Missing symbol"
        if shares is "":
            return "Missing shares"
        self.stock.symbol = symbol
        stockinfo = self.stock.lookup()
        if stockinfo is False:
            return "Invalid symbol."
        sale = self.portfolio.sell(self.user, self.stock, shares)
        return sale


