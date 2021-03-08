"""Script that populates the database with fake data

Feel free to add your own generators :-)
"""

#impoprt modules
from database import engine
from session import session

from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory
from models.Category import Category

from decimal import Decimal
from random import uniform


#ADD USERS = ===========================================
session.add_all([
     User(name='Zbyszek'),
     User(name='Krzysiek'),
     User(name='Mariola')
     ])

#Zapisz do bazy
session.commit()

#ADD BUDGETS

budget_list = []

x = 1
for n in range(3):
     budget_list.append(Budget(name="Mój budżet", user_id=x))
     x += 1

session.add_all(budget_list)
session.commit()

#ADD PARENT CATEGORIES

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

#ADD CATEGORIES

category_list = []

# parent_category_names = ["Rachunki", "Kredyty", "Wydatki na życie", "Odkładanie", "Rozrywki"]
category_names = [
     ["Prąd", "Internet", "Telefon", "Telewizja", "Woda", "Czynsz", "Gaz"],
     ["Kredyt studencki", "Kredyt w baku", "Kredyt hipoteczny", "Samochód"],
     ["Artykuły spożywcze", "Artykuły higieniczne"],
     ["Na remont łazienki", "Na wakacje", "Skarbonka"],
     ["Restauracja", "Kino"]
]

# loop through users
for u in range(3):
     #loop through budgets
     for b in range(3):
          #loop through parent categories
          for instance in session.query(ParentCategory).order_by(ParentCategory.id):
               #create categories based on list of names
               index = parent_category_names.index(instance.name)
               for c in range(len(category_names[index])):
                    category_list.append(Category(
                         name = category_names[index][c],
                         budgeted_amount = round(uniform(30.0, 2500.0), 2),
                         available_amount = round(uniform(0.0, 1300.0), 2),
                         parent_id = instance.id
                    ))

session.add_all(category_list)
session.commit()