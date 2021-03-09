"""Package that is responsible for application's internal logic

It is induced by main.py
"""

# from models.Base import Base
from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory
from models.Category import Category
from models.Transaction import Transaction

from session import session

from getpass import getpass
import hashlib
import os

from sqlalchemy.orm import lazyload

# GLOBAL VARIABLES
global_user_id = None
global_user_name = None


# DEFINE LOGIC HERE

# Display login form
def login():
    # Ask you user if they have an account
    answer = input("Do you have an account?[y/n]: ")

    # If user does not have an account, redirect them to create_account function
    if answer.lower() == 'n' or answer.lower() == 'no':
        print("\nSo, let's set up an account for you, then! :-)")
        create_account()

    # If user does have an account, ask them for login credentials
    elif answer.lower() == 'y' or answer.lower() == 'yes':
        print("\nAlright, let's log you in!")
        username = input("Username: ")
        password = getpass(prompt="Password: ")
        validate_login(username, password)

    # If user does not cooperate
    else:
        print("\nHmm, let's try again!")
        login()


# Create account
def create_account():
    # Prompt user for username
    username = input("Choose your username: ")

    # Check if username is not taken
    user_account = session.query(User).filter_by(name=username).first()
    while user_account is not None:
        print("\nHmm, that username is already taken! Let'stry something different.")
        username = input("Choose your username: ")
        user_account = session.query(User).filter_by(name=username).first()

    # Prompt user for password
    password = getpass(prompt="Great, choose your password now: ")

    # Hash password
    salt = os.urandom(32)  # A new salt for this user
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    # Create user
    user = User(name=username, salt=salt, key=key)
    session.add(user)
    session.commit()

    # Get user instance from db
    user_instance = session.query(User).filter_by(name=username).first()
    print("\nYou've sucessfully created the account!")

    # Redirect logged user
    set_global_variables(user_instance)


def validate_login(username, password):
    # Get user instance
    user_instance = session.query(User).filter_by(name=username).first()

    # Wrong username
    if user_instance is None:
        print("\nWrong password / username. Let's try again!")
        login()

    # Correct username
    else:

        # Retrieve user's salt and key
        salt = user_instance.salt
        key = user_instance.key

        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        # Check if the password is correct
        if key != new_key:
            print("\nWrong password / username. Let's try again!")
            login()
        # Correct password
        else:
            # Redirect logged user
            set_global_variables(user_instance)


# Set global variables, redirect
def set_global_variables(user_instance):
    # refer to global variables inside function
    global global_user_id
    global global_user_name

    global_user_id = user_instance.id
    global_user_name = user_instance.name
    show_budget()


# Show user's budget
def show_budget():
    # refer to global variables inside function
    global global_user_id
    global global_user_name

    print("\n{}, here's your budget!".format(global_user_name))
    budget_instance = session.query(Budget).filter_by(user_id=global_user_id).first()
    if budget_instance is None:
        print("Whoops, you don't have any budgets yet. :-(")
    else:
        # To zapytanie zwraca listę budżetów.
        # Wpisanie list_of_user_budgets[0].parent_categories zwraca listę parent kategorii pierwszego budżetu na liście
        # list_of_user_budgets[0].parent_categories[0].categories zwraca listę kategorii i tak dalej
        list_of_user_budgets = session.query(Budget).filter_by(user_id=global_user_id).options(
            lazyload(Budget.parent_categories).subqueryload(ParentCategory.categories)).all()

        # LOAD WHOLE BUDGET
        print("\n{}".format(list_of_user_budgets[0].name.upper()))

        # loop through parent categories
        for parent in list_of_user_budgets[0].parent_categories:
            # Calculate avaialbale amount based on category.avaialable_amount
            sum = 0.00
            # Loop through categories to calculate sum
            for category in parent.categories:
                sum += category.available_amount
            formatted_sum = "{:.2f} zł".format(sum)
            print("\n---------------- {}, dostępna kwota: {} ---------------- \n".format(parent.name, formatted_sum))

            # Loop tgrough ONCE AGAIN to print them
            n = 1  # Number of category within the parent
            for category in parent.categories:
                formatted_available = "{:.2f} zł".format(category.available_amount)
                print("{}. {}, dostępne środki: {}".format(n, category.name, formatted_available))
                n += 1  #Increment the category number

        print("\n")  # Print space between the next command
