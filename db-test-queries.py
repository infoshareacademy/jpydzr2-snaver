"""Test SQL queries, relations and debug it here

Feel free to add your own queries :-)
Don't forget to import the modules
"""

from sqlalchemy.orm import lazyload

from models.Budget import Budget
from models.Category import Category
from models.ParentCategory import ParentCategory
from models.Transaction import Transaction
from models.User import User
from session import session

# Retrieve a User object with a name 'Krzysiek'
get_user = session.query(User).filter_by(name='Krzysiek').first()

# Does it work?
print(get_user)

# Loop through all Users
for instance in session.query(User).order_by(User.id):
    print(instance)

# Loop through Budgets
for instance in session.query(Budget).order_by(Budget.id):
    print(instance)

# Loop through first 5 parent categories
for instance in session.query(ParentCategory).order_by(ParentCategory.id).limit(5):
    print(instance)

# Loop through first 5 categories
for instance in session.query(Category).order_by(Category.id).limit(5):
    print(f"Available amount: {instance.available_amount}")
    instance.budgeted_amount += 1000
    print(f"Available amount: {instance.available_amount}")
    print(f"Transactions in category {instance.id}: {instance.get_transactions()}")
    print(instance)

# Loop through first 5 transactions
for instance in session.query(Transaction).order_by(Transaction.id).limit(5):
    print(instance)

# Count categories
number_of_categories = session.query(Category).count()
print("Number of categories: {}.".format(number_of_categories))

# Count Transactions
number_of_transactions = session.query(Transaction).count()
print("Number of transactions: {}.".format(number_of_transactions))


# Relationships
users = session.query(User).options(lazyload(User.budgets).subqueryload(Budget.parent_categories).subqueryload(
    ParentCategory.categories)).all()
print(type(users))
print(users[1].budgets[0].parent_categories[0].categories)