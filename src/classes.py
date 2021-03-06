from __future__ import annotations
from datetime import datetime
import click  # https://www.roadsi.de/blog/python-and-keyboard-events/

# pierwsza klasa najbardziej rozpisana, reszta bedzie pewnie podobnie
# czy my zawsze będziemy chieli robić obiekty klas? Czasem na pewno, ale czy zawsze?


class Account:
    def __init__(self, name):
        print("Connect to DB and create account")
        self.__name = name
        self.__id = f"INSERT INTO TABELA {name}; select id ostatniego wpisu;"

    # @property name, @name.setter?

    @property
    def id(self):
        return self.__id

    @property
    def amount(self):
        return "SELECT SUM(TRANSFERY) - SUM(WYDATKI) FROM TABLE JOIN OTHER_TABLE"

    @property
    def unbudgeted_amount(self):
        return self.amount - "SELECT SUM(BUDGETS) FROM ANOTHER_TABLE"

    def get_budgets(self):
        return [f"SELECT BUDGETS WHERE ACCOUNT_ID = {self.id}"]

    def get_transfers(self, start_time: datetime, end_time: datetime):
        return [f"SELECT TRANSFERS WHERE ID={self.id} AND DATETIME BETWEEN ({start_time},{end_time})"]

    def get_spending(self):
        pass  # jak wyzej


class Transfer:
    def __init__(self, account: Account, amount, name):
        # tu jakaś walidacja tych wartości i wrzucanie ich go bazy
        if account > 0:
            self.__direction = "Wpływ"
        else:
            self.__direction = "Wypływ"
        self.__amount = amount
        self.name = name
        self.account = account
        self.date = datetime.now()


class Category:
    def __init__(self, name):
        print("Connect to DB and create category")
        self.__name = name
        self.__id = f"INSERT INTO TABELA {name}; GET LAST ENTRY ID"

    # @property id
    # @name.setter ubdate na bazie

    def get_spendings(self):
        return "z bazy wszystkie wydatki z tym id"


class Budget:
    def __init__(self, name, account: Account, amount=0):
        print("Connect to DB and create budget")
        self.__name = name
        self.__id = f"INSERT INTO TABELA {name}; GET LAST ENTRY ID"
        self.__amount = amount
        self.__account_id = account.id

    # @property id, account_id # nie edytowalne
    # @amount.setter: nie moze byc mniej niz 0
    # @name.setter: ubdate na bazie


class Spending:
    def __init__(self, category: Category, account: Account, amount, name):
        self.__category_id = category.id
        self.amount = amount
        self.name = name
        self.account_id = account.id


class Interface:
    def run(self):
        current_menu = None
        key = None
        while True:
            current_menu = self.display(current_menu, key)
            key = click.getchar()  # https://www.roadsi.de/blog/python-and-keyboard-events/ ??


if __name__ == "__main__":
    interface = Interface()
    interface.run()
