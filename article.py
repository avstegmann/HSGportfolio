from articleDAO import ArticleDAO
from apiACCESS import Api

dao = ArticleDAO()
api = Api()


class Article:

    source = None
    title = None
    description = None
    link = None
    image = None
    date = None

    def init_new(self, source, title, description, link, image, date, stock):
        self.source = source
        self.title = title
        self.description = description
        self.link = link
        self.image = image
        self.date = date
        dao.save_article(self, stock)

    def init_exist(self, source, title, description, link, image, date):
        self.source = source
        self.title = title
        self.description = description
        self.link = link
        self.image = image
        self.date = date

    def init_json(self):
        out = {
            'source': self.source,
            'title': self.title,
            'description': self.description,
            'link': self.link,
            'image': self.image,
            'date': self.date
        }
        return out

    def lookup(self, stock, date):
        """
        INPUT:  - object stock
                - today's date
        OUTPUT: - True
                - False
        """
        articles = {}

        # check if there are articles on the DB from today.
        check = dao.get_articles(stock.ID, date)
        if check is False:
            news = api.news_lookup(stock.name, date)
            amount_news = int(len(news))
            for i in range(0, amount_news):
                self.init_new(
                    news[i][0]['source'],
                    news[i][0]['title'],
                    news[i][0]['description'],
                    news[i][0]['link'],
                    news[i][0]['image'],
                    news[i][0]['date'],
                    stock
                )
                articles[i] = [self.init_json()]

            if amount_news < 3:
                old = dao.get_old_articles(stock.ID)
                for k in range(0, 3-amount_news):
                    try:
                        self.init_exist(
                            old[k][0],
                            old[k][1],
                            old[k][2],
                            old[k][3],
                            old[k][4],
                            old[k][5],
                        )
                    except IndexError:
                        self.init_exist("", 'No news available', "", "", "", "")
                    finally:
                        articles[k] = [self.init_json()]
            return articles
        else:
            for k in range(0, len(check)):
                if check is False:
                    self.title = 'No news available.'
                else:
                    self.init_exist(
                        check[k][0],
                        check[k][1],
                        check[k][2],
                        check[k][3],
                        check[k][4],
                        check[k][5],
                    )
                articles[k] = [self.init_json()]
            return articles

