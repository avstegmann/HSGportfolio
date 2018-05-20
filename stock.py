from apiACCESS import Api
from stockDAO import StockDAO

dao = StockDAO()
api = Api()


class Stock:

    ID = None
    currency = None
    name = None
    price = None
    symbol = None

    def new_stock(self, stockinfo):
        """
        INPUT: stockinfo    -> api query
        OUTPUT: None        -> stock is initialized and a new entry is saved in the DB
        """

        self.currency = stockinfo[self.symbol][0]['currency']
        self.name = stockinfo[self.symbol][0]['name']
        self.price = stockinfo[self.symbol][0]['price']
        check = dao.new_stock(self)
        if check is not True:
            return check
        self.ID = dao.stock_info(self)[0]
        return True

    def lookup(self):
        """
        - check if the symbol is already in DB -> initialize it with real time price
        - if not:
            check if the symbol exist in the API
            get information from yahoo -> real time information
        """
        if dao.check_stock(self):
            self.init(dao.stock_info(self))
            self.price = api.simple_lookup(self.symbol)[self.symbol][0]['price']
            dao.update_stock_prices([self.price], [self.symbol])
            return True
        else:
            stockinfo = api.simple_lookup(self.symbol)
            if stockinfo is False:
                return "Invalid symbol"
            else:
                out = self.new_stock(stockinfo)
                if out is not True:
                    return out
                return True

    def init(self, info):
        self.ID = info[0]
        self.currency = info[1]
        self.name = info[2]
        self.price = info[3]

    @staticmethod
    def symbols(user):
        """
        RETURN: List of symbols for stocks owned by user
        (used in drop down menu for sell page)
        """
        return dao.get_symbols(user)

    @staticmethod
    def update():
        """
        - Get symbols from all stocks
        - Split the string
        - Run multiple API calls
        - Update prices in DB
        """
        # Get symbols from all stocks and arrange them as API compatible string
        info = dao.stock_info_all()
        length = len(info)
        # Arrange symbols in arrays of 10
        for i in range(0, length, 10):
            symbols = info[i:i+10]
            # Iterate over symbols
            query = str(symbols[0][2])
            for k in range(1, len(symbols)):
                query = query + "," + str(symbols[k][2])
            # Make API queries
            new_info = api.get_prices(query)
            # Update DB
            prices_dao = []
            symbols_dao = []
            for m in range(0, len(new_info)):
                prices_dao.append(new_info[m][0]['price'])
                symbols_dao.append(new_info[m][0]['symbol'])
            dao.update_stock_prices(prices_dao, symbols_dao)
