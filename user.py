from userDAO import UserDAO

dao = UserDAO


class User:

    ID = None
    expenses = None
    current = None
    cash = None
    username = None
    password = None

    def login(self):
        check = dao.check_pass(dao, self)
        if check is True:
            self.init()
            return True
        else:
            return check

    def new_user(self):
        check = dao.check_reg(dao, self)
        if check is True:
            self.init()
            return True
        else:
            return check

    def init(self):
        info = dao.user_info(self)
        self.ID = info[0]
        self.cash = info[3]
        self.expenses = info[4]
        self.current = info[5]

    def update(self, totalexpenses, totalcurrent):
        dao.update(self, totalexpenses, totalcurrent)
        self.expenses = totalexpenses
        self.current = totalcurrent

    def update_cash(self):
        cash = dao.update_user_cash(self)
        self.cash = cash

    @staticmethod
    def get_usernames():
        return dao.get_usernames()
