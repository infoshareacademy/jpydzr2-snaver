"""Package that is responsible for application's internal logic

It is induced by main.py
"""

from models.Base import Base
from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory

from session import session

from getpass import getpass
import hashlib
import os

# GLOBAL VARIABLES
global_user_id = None
global_user_name = None


# DEFINE LOGIC HERE

# Display login form
def login():
    # Welcome message
    print("\nWelcome to Snaver!\n")

    #Ask you user if they have an account
    answer = input("Do you already have an account?[y/n]: ")

    # If user does not have an account, redirect them to create_account function
    if answer.lower() == 'n' or answer.lower() == 'no':
        print("\nSo, let's set up an account for you, then! :-)\n")
        create_account()

    # If user does have an account, ask him for login credentials
    elif answer.lower() == 'y' or answer.lower() == 'yes':
        print("Alright, let's log you in!\n")
        username = input("Username: ")
        password = getpass(prompt="Password: ")
        validate_login(username, password)

    # If user's input is somehow... weird
    else:
        print("Hmm, let's try again!\n")
        login()


def validate_login(username, password):
    #get user instance
    user_instance = session.query(User).filter_by(name=username).first()
    if user_instance is None:
        print("Wrong password / username. Let's try again!")
        login()
    else:
        salt = user_instance.salt  # Get the salt
        key = user_instance.key  # Get the correct key

        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        if key != new_key:
            print("Wrong password / username. Let's try again!")
            login()
        else:
            get_user(user_instance)


# Set global variables, redirect
def get_user(user_instance):
    # refer to global variables inside function
    global global_user_id
    global global_user_name

    global_user_id = user_instance.id
    global_user_name = user_instance.name
    show_budget()

# Create account
def create_account():
    username = input("Choose your username: ")
    does_user_exist = session.query(User).filter_by(name=username).first()
    while does_user_exist is not None:
        print("Hmm, that username is already taken! Let'stry something different.\n")
        username = input("Choose your username: ")
        does_user_exist = session.query(User).filter_by(name=username).first()
    password = getpass(prompt="Great, choose your password now: ")

    # Hash password
    salt = os.urandom(32)  # A new salt for this user
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    user = User(name=username, salt=salt, key=key)
    session.add(user)
    session.commit()

    print("You've sucessfully created the account!")

    # set global variables through get_user function
    login()


# Show user's budget
def show_budget():
    # refer to global variables inside function
    global global_user_id
    global global_user_name

    print("\nHej, {}, oto Twój budżet!\n".format(global_user_name))
    budget_instance = session.query(Budget).filter_by(user_id=global_user_id).first()
    print(budget_instance)

    # TODO
