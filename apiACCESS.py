import requests
import json


class Api:
    @staticmethod
    def simple_lookup(symbols):
        """
        INPUT: Takes str with stock symbols
        OUTPUT: - True, Returns currency, name and price of each stock as a dict
                - False
        """
        with requests.session():
            url = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols={}'.format(symbols)
            info = requests.get(url)
        if not info:
            return False
        else:
            info = info.json()
            # print(json.dumps(info, indent=2))
            output = {}
            for i in range(0, len(info['quoteResponse']['result'])):
                key = info['quoteResponse']['result'][i]['symbol']
                try:
                    name = info['quoteResponse']['result'][i]['longName']
                except KeyError:
                    name = info['quoteResponse']['result'][i]['shortName']
                output[key] = [
                    {
                        'currency': info['quoteResponse']['result'][i]['currency'],
                        'name': name,
                        'price': info['quoteResponse']['result'][i]['regularMarketPrice']
                    }
                ]
            return output

    @staticmethod
    def get_prices(symbols):
        """
        INPUT: symbols
        OUTPUT: current price
        """
        with requests.session():
            url = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols={}'.format(symbols)
            info = requests.get(url)
        if not info:
            return False
        else:
            info = info.json()
            output = {}
            for i in range(0, len(info['quoteResponse']['result'])):
                output[i] = [{
                    'symbol': info['quoteResponse']['result'][i]['symbol'],
                    'price':  info['quoteResponse']['result'][i]['regularMarketPrice']
                }]
            return output

    @staticmethod
    def news_lookup(company, date):
        """
        INPUT: Takes str with stock symbol
        OUTPUT: - True, returns publisher, title and hyperlink, maximal 3 articles
                - False
        """
        with requests.session():
            url = 'https://newsapi.org/v2/everything?q={company}&from={date}&to={date}&language=en&sortBy=popularity&' \
                  'apiKey=88404ebbb56c4cc78cd7206b2027a138'.format(company=company, date=date)
            info = requests.get(url)
        if info:
            info = info.json()
            output = {}
            amount_news = int(len(info["articles"]))
            if amount_news >= 3:
                amount_news = 3
            for i in range(0, amount_news):
                key = i
                output[key] = [
                    {
                        'source': info["articles"][i]["source"]["name"],
                        'title': info["articles"][i]["title"],
                        'description': info["articles"][i]["description"],
                        'link': info["articles"][i]["url"],
                        'image': info["articles"][i]["urlToImage"],
                        'date': date
                    }
                ]
            return output
        else:
            return False

    @staticmethod
    def currency_lookup_single(currencypair):
        """
        INPUT: Takes currency pair for exchange rate
        OUTPUT: - True, returns chosen currency pair & rate
                - False
        """
        with requests.session():
            url = 'https://forex.1forge.com/1.0.3/quotes?pairs={}' \
                  '&api_key=p2nuuJJrHWg7J0B951Pf7iMADx1Gfy2w'.format(currencypair)
            info = requests.get(url)

        if info:
            info = info.json()
            output = [
                {
                    'symbol': info[0]['symbol'],
                    'price': info[0]['price']
                }
            ]
            return output
        else:
            return False

    @staticmethod
    def currency_lookup_full():
        """
        INPUT: ---
        OUTPUT: - CHFEUR, EURCHF, CHFUSD, USDCHF
                - False
        """
        with requests.session():
            url = 'https://forex.1forge.com/1.0.3/quotes?pairs=CHFEUR,EURCHF,CHFUSD,USDCHF' \
                  '&api_key=p2nuuJJrHWg7J0B951Pf7iMADx1Gfy2w'
            info = requests.get(url)

        if info:
            info = info.json()
            output = {}
            for i in range(0, 4):
                key = info[i]['symbol']
                output[key] = [
                    {
                        'price': info[i]['price'],
                    }
                ]
            return output
        else:
            return False
