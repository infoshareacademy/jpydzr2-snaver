"""Package that is responsible for application's internal logic

It is induced by main.py
"""

import hashlib
import os
from getpass import getpass

from sqlalchemy.orm import lazyload
import datetime

from models.Budget import Budget
from models.Category import Category
from models.ParentCategory import ParentCategory
from models.Transaction import Transaction
from models.User import User
from session import session

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

        # Validate the login credentials
        validate_login(username, password)

    # If user does not cooperate
    else:
        print("\nHmm, let's start over!")
        login()


# Create account
def create_account():
    # Prompt user for username
    username = input("Choose your username: ")

    # Check if username is not taken
    user_account = session.query(User).filter_by(name=username).first()
    while user_account is not None:
        print("\nHmm, that username is already taken. Let's try something different!")
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
    print("\nYou've successfully created the account!")

    # Redirect logged user
    set_global_variables(user_instance)


# Validate the login credentials
def validate_login(username, password):
    # Get user instance
    user_instance = session.query(User).filter_by(name=username).first()

    # Wrong username
    if user_instance is None:
        print("\nWrong password / username. Let's try again!")
        login()

    # else == Correct username
    else:

        # Retrieve user's salt and key
        salt = user_instance.salt
        key = user_instance.key

        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        # Check if the password is correct
        if key != new_key:
            print("\nWrong password / username. Let's try again!")
            login()

        # else == Correct password
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

    # Redirect the user to their budgets
    show_budget()


# Show user's budget
def show_budget():
    # refer to global variables inside function
    global global_user_id
    global global_user_name

    # Try to retrieve the user's budget
    budget_instance = session.query(Budget).filter_by(user_id=global_user_id).first()

    # If user has no budgets
    if budget_instance is None:
        print("\nWhoops, you don't have any budgets yet. Shall we create one?")
        adding_budget()
    # else == User does have at least 1 budget
    else:
        # Welcome message
        print("\n{}, here's your budget!".format(global_user_name))

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


def adding_budget():
    global global_user_id
    budget_name = input("Nazwij swój budżet:")
    budget = Budget(name=budget_name, user_id=global_user_id)
    session.add(budget)
    session.commit()
    show_budget()



def add_transaction():

    transaction_name = input("Podaj nazwe transakcji:")
    transaction_payee_name = input("Podaj nazwę sklepu lub płatnika: ")
    transaction_amount_inflow = float(input("Podaj kwotę wpływu:"))
    transaction_amount_outflow = float(input("Podaj kwotę wydatku: "))
    transaction_category_id = int(input("Podaj id kategorii"))

    transaction = Transaction(name=transaction_name,payee_name=transaction_payee_name,
                             amount_inflow=transaction_amount_inflow, amount_outflow=transaction_amount_outflow,
                             category_id=transaction_category_id)
    session.add(transaction)
    session.commit()


