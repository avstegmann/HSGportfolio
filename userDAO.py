from masterDAO import Connection
from argon2 import *

connection = Connection()
ph = PasswordHasher()


class UserDAO:

    @staticmethod
    def user_info(user):
        """
        INPUT: user
        OUTPUT: All data from the corresponding row in the database
        """
        try:
            db = connection.getcursor()
            sql = "SELECT * FROM users WHERE username=%s"
            db.execute(sql, [user.username])
            info = db.fetchone()
            return info
        finally:
            pass

    @staticmethod
    def check_user(user):
        """
        INPUT: user
        Check if user is registered.
        RETURN: - True
                - False
        """
        try:
            db = connection.getcursor()
            sql = "SELECT EXISTS(SELECT * FROM users WHERE username=%s)"
            db.execute(sql, [user.username])
            if db.fetchone()[0]:
                return True
            else:
                return False
        finally:
            pass

    @staticmethod
    def update(user, totalexpenses, totalcurrent):
        db = connection.getcursor()
        try:
            sql = "UPDATE users SET totalexpenses=%s, totalcurrent=%s " \
                  "WHERE userID=%s"
            db.execute(sql, [totalexpenses, totalcurrent, user.ID])
        finally:
            connection.getcnx().commit()

    @staticmethod
    def update_user_cash(user):
        db = connection.getcursor()
        try:
            sql = "SELECT cash FROM users " \
                  "WHERE userID=%s"
            db.execute(sql, [user.ID])
            return db.fetchone()[0]
        finally:
            connection.getcnx().commit()

    @staticmethod
    def get_usernames():
        db = connection.getcursor()
        try:
            sql = "SELECT username FROM users"
            db.execute(sql)
            return db.fetchall()
        finally:
            pass

    def check_pass(self, user):
        """
        INPUT: user
        Check if user ist registered.
        RETURN: - True
                - Wrong username or password (with distinction)
        """

        if self.check_user(user) is True:
            db = connection.getcursor()
            sql = "SELECT password FROM users WHERE username=%s"
            db.execute(sql, [user.username])
            try:
                ph.verify(db.fetchone()[0], user.password)
                return True
            except exceptions.VerifyMismatchError:
                return "Wrong password."
            finally:
                pass
        else:
            return "Wrong username."

    def check_reg(self, user):
        """
        INPUT: user that is not in DB
        Check if the given username is already in use. If not create new entry in DB.
        OUTPUT: If there is no other user with the same name -> True, else False/'This username already exists.'
        """
        check = self.check_user(user)
        if check is True:
            return "This username already exists."
        else:
            try:
                db = connection.getcursor()
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                db.execute(sql, [user.username, ph.hash(user.password)])
                return True
            finally:
                connection.getcnx().commit()

