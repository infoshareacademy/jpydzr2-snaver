import hashlib
import os
from getpass import getpass

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