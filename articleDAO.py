from masterDAO import Connection
import datetime

connection = Connection()


class ArticleDAO:

    @staticmethod
    def check_articles(ID, date):
        """
        INPUT: symbol, date
        Check if there are news articles for this symbol from today.
        RETURN: - True
                - False
        """
        try:
            db = connection.getcursor()
            sql = "SELECT EXISTS(SELECT * FROM articles WHERE " \
                  "stockID=%s and date=%s);"
            db.execute(sql, [ID, date])
            check = db.fetchone()[0]
            if check:
                return True
            else:
                return False
        finally:
            pass

    @staticmethod
    def check_source(source):
        """
        INPUT: source
        Check if the source is already stored
        RETURN: - True
                - False
        """
        try:
            db = connection.getcursor()
            sql = "SELECT EXISTS(SELECT * FROM sources WHERE " \
                  "source=%s);"
            db.execute(sql, [source])
            if db.fetchone()[0]:
                return True
            else:
                return False
        finally:
            pass

    def get_articles(self, ID, date):
        db = connection.getcursor()
        if self.check_articles(ID, date) is True:
            try:
                sql = "SELECT b.source, a.title, a.description, a.link, a.image, a.date " \
                      "FROM articles a JOIN sources b ON a.sourceID = b.sourceID " \
                      "WHERE a.stockID=%s " \
                      "ORDER BY a.date DESC " \
                      "LIMIT 3;"
                db.execute(sql, [ID])
                articles = db.fetchall()
                return articles
            finally:
                pass
        else:
            return False

    def get_old_articles(self, ID):
        db = connection.getcursor()
        try:
            sql = "SELECT b.source, a.title, a.description, a.link, a.image, a.date " \
                  "FROM articles a JOIN sources b ON a.sourceID = b.sourceID " \
                  "WHERE a.stockID=%s " \
                  "LIMIT 3;"
            db.execute(sql, [ID])
            articles = db.fetchall()
            return articles
        finally:
            pass

    def save_article(self, article, stock):
        db = connection.getcursor()
        if not self.check_source(article.source):
            try:
                sql = "INSERT INTO sources (source) VALUES (%s)"
                db.execute(sql, [article.source])
            finally:
                connection.getcnx().commit()
        try:
            sql = 'INSERT INTO articles ' \
                  '(stockID, sourceID, title, description, link, image, date) ' \
                  'VALUES (' \
                  '%s, (SELECT sourceID FROM sources WHERE source=%s),' \
                  '%s, %s, %s, %s, %s);'
            db.execute(sql, [stock.ID, article.source, article.title, article.description, article.link,
                             article.image, datetime.datetime.now().date()])
        finally:
            connection.getcnx().commit()
