import random
from config import USERS


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class Data:
    purchase = None
    amount = None
    currency = None
    user = None

    @classproperty
    def purchase(self):
        purchase = random.randint(1, 1000)
        return purchase

    @classproperty
    def amount(self):
        amount = round(random.uniform(10.5, 7500.5), 2)
        return amount

    @classproperty
    def currency(self):
        currency = random.choice(["USD", "EUR", "GBP"])
        return currency

    @classproperty
    def user(self):
        user = random.choice(USERS)
        return user
