from portfolioDAO import PortfolioDAO
from apiACCESS import Api

dao = PortfolioDAO()
api = Api()


class Portfolio:

    rows = {}
    history = {}
    exchange_rates = {}

    def update(self, user):
        """
        INPUT: user
        - get number of rows in Portfolio
        - build dictionary with current values from DB
        Output: update self.rows
        """
        self.rows = {}
        self.get_exchange_rates()
        info = dao.get_info(user)
        total_expenses = 0
        total_current = 0
        for i in range(0, len(info)):
            self.rows[i] = [
                {
                    'name': info[i][0],
                    'shares': info[i][1],
                    'buyingprice': round(info[i][2], 2),
                    'currency': info[i][3],
                    'exchange_rate': info[i][4],
                    'expenses': round(info[i][5], 2),
                    'cprice': round(info[i][6], 2),
                    'cvalue': round(info[i][7], 2),
                    'net': round(info[i][7]-info[i][5], 2),
                    'net_perc': round((info[i][7]-info[i][5])*100/info[i][5], 2)
                }
            ]
            if info[i][3] == 'CHF':
                total_expenses += info[i][5]
                total_current += info[i][7]
            elif info[i][3] == 'USD':
                total_expenses += info[i][5] * info[i][4]
                total_current += info[i][7] * self.exchange_rates[0][0]['USDCHF']
            elif info[i][3] == 'EUR':
                total_expenses += info[i][5] * info[i][4]
                total_current += info[i][7] * self.exchange_rates[0][0]['EURCHF']
        self.rows['A'] = [{'ctotal_value': round(total_current, 2)}]
        total_current += user.cash
        user.update(total_expenses, total_current)
        if len(self.rows) == 0:
            return False
        return True

    def update_user(self, user):
        """
        Used for hourly update.
            - update exchange rates
            - update user.current, user.expenses -> this leads to an up to date leaderboard
        """
        self.update_exchange_rates()
        info = dao.get_info(user)
        total_expenses = 0
        total_current = user.cash
        for i in range(0, len(info)):
            if info[i][3] == 'CHF':
                total_expenses += info[i][5]
                total_current += info[i][7]
            elif info[i][3] == 'USD':
                total_expenses += info[i][5] * info[i][4]
                total_current += info[i][7] * self.exchange_rates[0][0]['USDCHF']
            elif info[i][3] == 'EUR':
                total_expenses += info[i][5] * info[i][4]
                total_current += info[i][7] * self.exchange_rates[0][0]['EURCHF']
        user.update(total_expenses, total_current)

    def buy(self, user, stock, shares):
        """
        INPUT: user, stock # of shares
        - save the stockinfo to DB if it is not already in it
        - get real time exchange rates from API     --->    update entry in DB

        - check if user can afford the purchase
        - save # of shares in users portfolio
        - calculate expenses
        - calculate user.cash
        - commit price and exchange rate

        OUTPUT: - True (if purchase was successful)
                - False (+ error message)
        """

        if stock.currency == 'CHF':
            pair = None
            rate = 1
            if float(stock.price) * float(shares) > float(user.cash):
                return 'Not enough cash.'
        else:
            pair = str(stock.currency) + 'CHF'
            rate = api.currency_lookup_single(pair)[0]['price']  # -> Fehlermeldung
            if float(stock.price) * float(shares) * float(rate) > float(user.cash):
                return 'Not enough cash.'
            self.update_exchange_rate(pair, rate)
        check = dao.check(stock, user)
        if check is 1:
            dao.buy_merge(user, stock, shares, pair, rate)
        else:
            dao.buy_new(user, stock, shares, pair, rate)
        user.update_cash()
        return True

    def sell(self, user, stock, shares_sold):
        """
        INPUT: user, stock # of shares
        - get real time exchange rates from API     --->    update entry in DB

        - check if user is able to sell # of shares
        - save # of shares in users portfolio
        - calculate cash
        - calculate user.cash
        - commit price and exchange rate

        OUTPUT: - True (if sale was successful)
                - False (+ error message)
        """
        shares = dao.get_shares(user, stock)                     # -> Drop Down Liste mit Stocks im Portfolio?
        if shares_sold > shares:
            return 'Not enough shares.'
        if stock.currency is not 'CHF':
            pair = 'CHF' + str(stock.currency)
            rate = api.currency_lookup_single(pair)[0]['price']                           # -> Fehlermeldung ausdrucken?
            self.update_exchange_rate(pair, rate)
        else:
            pair = None
            rate = 1
        if shares_sold < shares:
            dao.sell_part(user, stock, shares_sold, (shares-shares_sold), pair, rate)
        else:
            dao.sell_all(user, stock, shares, pair, rate)
        user.update_cash()
        return True

    def get_history(self, user):
        self.history = {}
        info = dao.get_history(user)
        for i in range(0, len(info)):
            self.history[i] = [
                {
                    'date': str(info[i][0]),
                    'name': info[i][1],
                    'shares': round(info[i][2], 2),
                    'buyingprice': info[i][3],
                    'currency': info[i][4],
                    'value': round(info[i][5], 2),
                    'exchange_rate': info[i][6]
                }
            ]

    @staticmethod
    def update_exchange_rate(pair, rate):
        """
        INPUT:  The currency pair -> 'USDCHF', 'EURCHF', etc.
                The matching exchange rate, obtained by the API
        updates the entry in the DB
        """
        dao.update_exchange_rate(pair, rate)

    def get_exchange_rates(self):
        """
        Initializes the container exchange_rates
        """
        rates = dao.get_exchange_rates()
        self.exchange_rates[0] = [
            {
                'USDCHF': rates[0][2],
                'EURCHF': rates[1][2],
                'CHFUSD': rates[2][2],
                'CHFEUR': rates[3][2]
            }
        ]

    def update_exchange_rates(self):
        """
        updates the exchange rates in the DB
        """
        rates = api.currency_lookup_full()
        dao.update_exchange_rate('USDCHF', rates['USDCHF'][0]['price'])
        dao.update_exchange_rate('EURCHF', rates['EURCHF'][0]['price'])
        dao.update_exchange_rate('CHFUSD', rates['CHFUSD'][0]['price'])
        dao.update_exchange_rate('CHFEUR', rates['CHFEUR'][0]['price'])

        self.exchange_rates[0] = [
            {
                'USDCHF': rates['USDCHF'][0]['price'],
                'EURCHF': rates['EURCHF'][0]['price'],
                'CHFUSD': rates['CHFUSD'][0]['price'],
                'CHFEUR':rates['CHFEUR'][0]['price']
            }
        ]
