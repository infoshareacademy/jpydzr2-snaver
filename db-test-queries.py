"""Test SQL queries, relations and debug it here

Feel free to add your own queries :-)
Don't forget to import the modules
"""

from database import engine
from session import session
from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory
from models.Category import Category

#Retrive a User object with a name 'Krzysiek'
get_user = session.query(User).filter_by(name='Krzysiek').first()

#Does it work?
print(get_user)

#Loop through all Users
for instance in session.query(User).order_by(User.id):
    print(instance)

#Loop through Budgets
for instance in session.query(Budget).order_by(Budget.id):
    print(instance)

#Loop through all parent categories
for instance in session.query(ParentCategory).order_by(ParentCategory.id):
    print(instance)

#Loop through all parent categories
for instance in session.query(Category).order_by(Category.id):
    print(instance)

#Count parent categories
number_of_parent_categories = session.query(ParentCategory).count()
print("Number of parent categories: {}.".format(number_of_parent_categories))