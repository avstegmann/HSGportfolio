# Das ist das Beispielfile, wie man beispielsweise controller funktionen implementieren könnte.
from controller import Controller
import json
import datetime
import time

controller = Controller()

username = input("Username: ")
password = input("Password: ")
controller.login(username, password)

print(controller.lookup('AM'))


"""
yn = True
while yn is True:
    symbol = input("Lookup: ")
    check = controller.lookup(symbol)
    print(controller.stock.name + " (" + controller.stock.symbol + "), " + str(controller.stock.price))
    print(controller.articles)
    print(controller.articles[0][0]['title'])
    #print(controller.articles[1][0]['title'])
    #print(controller.articles[2][0]['title'])
    if input('Y/N?') == 'N':
        yn = False
"""

# resp = controller.buy('AAPL', 3)
# print(resp)

# print(controller.articles[0][0])
# register kommt aus controller -> user -> userDAO

# reg = controller.register(controller, username, password)
# print(reg)
# print(controller.user.ID, controller.user.username)

#output = controller.lookup(symbol)
#print(controller.articles[0].title)

# print(json.dumps(output, indent=3))
# print(controller.stock.symbol)

"""
print(lookup('GOOGL'))
"""

