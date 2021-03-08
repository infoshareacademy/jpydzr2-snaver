"""Package that is responsible for application's internal logic

It is induced by main.py
"""

from models.Base import Base
from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory

from session import session

# GLOBAL VARIABLES
global_user_id = None
global_user_name = None


# DEFINE LOGIC HERE

# Display login form
def login():
    username = input("Hello, what's your name?\n")
    get_user(username)


# Check if user exists, set global variables, redirect
def get_user(username):
    # refer to global variables inside function
    global global_user_id
    global global_user_name

    user_instance = session.query(User).filter_by(name=username).first()
    if user_instance is None:
        create_account(username)
    else:
        global_user_id = user_instance.id
        global_user_name = user_instance.name
        show_budget()


# Create account
def create_account(username):
    print("\nHi, {}, seems like you don't have an account. Worry not! We've just created one for you! :-)".format(
        username))
    user = User(name=username)
    session.add(user)
    session.commit()

    # set global variables through get_user function
    get_user(username)


# Show user's budget
def show_budget():
    # refer to global variables inside function
    global global_user_id
    global global_user_name

    print("Hej, {}, oto Twój budżet!".format(global_user_name))
    budget_instance = session.query(Budget).filter_by(user_id=global_user_id).first()
    print(budget_instance)

    # TODO
