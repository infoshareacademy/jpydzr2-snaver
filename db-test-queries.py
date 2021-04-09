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

transactions = session.query(Transaction).all()
print(transactions)

# Relationships
users = session.query(User).options(lazyload(User.budgets).subqueryload(Budget.parent_categories).subqueryload(
    ParentCategory.categories)).all()
print(type(users))
print(users[1].budgets[0].parent_categories[0].categories)

# Show user's budget
def show_budget():
    # Try to retrieve the user's budget
    global_user_id = 1   # =1 is just the example
    budget_instance = session.query(Budget).filter_by(user_id=global_user_id).first()

    # Welcome message
    # print(f"\n{global_user_id}, here's your budget!")

    # Get the list of all user's budgets and its children up to the category level
    budgets_list = session.query(Budget).filter_by(user_id=global_user_id).options(
        lazyload(Budget.parent_categories).subqueryload(ParentCategory.categories)).all()

    # Zapytanie wyżej zwraca listę budżetów zalogowanego użytkownika, w której są listy pod-dzieci
    # Wpisanie budgets_list[0].parent_categories zwraca listę parent kategorii pierwszego budżetu na liście
    # budgets_list[0].parent_categories[0].categories zwraca listę kategorii i tak dalej

    # print the name of the first budget on the list
    print("\n{}".format(budgets_list[0].name.upper()))  # Print first budget's name

    # LOAD WHOLE BUDGET

    # loop through parent categories of the first budget in the list
    for parent in budgets_list[0].parent_categories:

        # Start calculating the parent's available amount based its children' available_amount
        parent_available_sum = 0.00

        # Loop through the parent's categories to add available_amount to the parent_available_sum
        for category in parent.categories:
            parent_available_sum += category.available_amount

        # Format the result and print it along parent category's name
        formatted_sum = "{:.2f} zł".format(parent_available_sum)
        print("\n---------------- {}, dostępna kwota: {} ---------------- \n".format(parent.name, formatted_sum))

        # Loop through the categories of the parent ONCE AGAIN, this time to print them
        n = 1  # Position (number) of the category within the parent
        for category in parent.categories:
            formatted_available = "{:.2f} zł".format(category.available_amount)
            print("{}. {}, dostępne środki: {}".format(n, category.name, formatted_available))
            n += 1  # Increment the category number

    print("\n")  # Print space between the next command
show_budget()