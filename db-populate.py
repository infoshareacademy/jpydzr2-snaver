"""Script that populates the database with fake data

Feel free to add your own generators :-)
"""

#impoprt modules
from database import engine
from session import session

from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory

#from random import randint


#ADD USERS = ===========================================
session.add_all([
     User(name='Zbyszek'),
     User(name='Krzysiek'),
     User(name='Mariola')
     ])

#Zapisz do bazy
session.commit()

#ADD BUDGETS ===========================================
budget_list = []

x = 1
for n in range(3):
     budget_list.append(Budget(name="Mój budżet", user_id=x))
     x += 1

session.add_all(budget_list)
session.commit()

#ADD CATEGORIES = ===========================================
parent_category_list = []

parent_category_names = ["Rachunki", "Kredyty", "Wydatki na życie", "Odkładanie", "Rozrywki"]

u = 1
for i in range(3):
     x = 0
     for j in range(5):
          parent_category_list.append(ParentCategory(name=parent_category_names[x], budget_id=u))
          x += 1
     u += 1

session.add_all(parent_category_list)
session.commit()