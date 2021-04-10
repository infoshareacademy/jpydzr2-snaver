"""Script that populates the database with fake data

Feel free to add your own generators :-)
"""

import hashlib
import os
from datetime import datetime
from datetime import date
from datetime import timedelta

from random import randint
from random import uniform

from models.Budget import Budget
from models.Category import Category
from models.ParentCategory import ParentCategory
from models.Transaction import Transaction
from models.CategoryBudget import CategoryBudget
from models.User import User
from session import session

# ADD USERS
# ------------------------------

user_names = ["Zbyszek", "Krzysiek", "Mariola"]
user_list = []

for i in range(len(user_names)):
    salt = os.urandom(32)
    # Test users' passwords == "test"
    key = hashlib.pbkdf2_hmac('sha256', "test".encode('utf-8'), salt, 100000)
    # append user instance
    user_list.append(User(name=user_names[i], salt=salt, key=key))

# Zapisz do bazy
session.add_all(user_list)
session.commit()

# ADD BUDGETS
# ------------------------------

budget_list = []

for user_instance in session.query(User).order_by(User.id):
    budget_list.append(Budget(name="Budżet użytkownika {}".format(user_instance.name), user_id=user_instance.id))

session.add_all(budget_list)
session.commit()

# ADD PARENT CATEGORIES
# ------------------------------

parent_category_list = []
parent_category_names = ["Rachunki", "Kredyty", "Wydatki na życie", "Odkładanie", "Rozrywki"]

for budget_instance in session.query(Budget).order_by(Budget.id):
    for i in range(len(parent_category_names)):
        parent_category_list.append(ParentCategory(name=parent_category_names[i], budget_id=budget_instance.id))

session.add_all(parent_category_list)
session.commit()

# ADD CATEGORIES
# ------------------------------

category_list = []
category_names = [
    ["Prąd", "Internet", "Telefon", "Telewizja", "Woda", "Czynsz", "Gaz"],
    ["Kredyt studencki", "Kredyt w baku", "Kredyt hipoteczny", "Samochód"],
    ["Artykuły spożywcze", "Artykuły higieniczne"],
    ["Na remont łazienki", "Na wakacje", "Skarbonka"],
    ["Restauracja", "Kino"]
]

# loop through parent categories
for parent_instance in session.query(ParentCategory).order_by(ParentCategory.id):
    # create categories based on list of names
    index = parent_category_names.index(parent_instance.name)
    for c in range(len(category_names[index])):
        category_list.append(Category(
            name=category_names[index][c],
            # budgeted_amount=round(uniform(30.0, 2500.0), 2),  # PyCharm complains but it's expected behaviour because of getter-setter setup
            parent_id=parent_instance.id
        ))

session.add_all(category_list)
session.commit()

# ADD TRANSACTIONS
# ------------------------------

transaction_list = []
# loop through categories
for category_instance in session.query(Category).order_by(Category.id):
    for i in range(randint(1, 10)):
        transaction_list.append(Transaction(
            name="Transakcja",
            payee_name="Nazwa sklepu / płatnika",
            amount_inflow=0.00,
            amount_outflow=round(uniform(0.0, 800.0), 2),
            category_id=category_instance.id,
            receipt_date=date.today() + timedelta(randint(-60,60))
        ))

session.add_all(transaction_list)
session.commit()

# ADD CATEGORY BUDGETS
# ------------------------------

month = datetime.now().month
year = datetime.now().year
day = datetime.now().day

category_budgets_list = []

for category_instance in session.query(Category).order_by(Category.id):
    category_budgets_list.append(CategoryBudget(
        budgeted_amount=round(uniform(30.0, 2500.0), 2),
        # PyCharm complains but it's expected behaviour because of getter-setter setup
        category_id=category_instance.id,
        datetime=datetime(year, month, day)
    ))

session.add_all(category_budgets_list)
session.commit()
