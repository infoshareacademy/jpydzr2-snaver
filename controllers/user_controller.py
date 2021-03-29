import hashlib
import os
from getpass import getpass

from models.User import User
from session import session
from .budget_controller import change_budget


# Display login form
def login() -> User:
    answer = input("Do you have an account?[y/n]: ")

    # If user does not have an account, redirect them to create_account function
    if answer.lower() == 'n' or answer.lower() == 'no':
        print("\nSo, let's set up an account for you, then! :-)")
        user = create_account()

    # If user does have an account, ask them for login credentials
    elif answer.lower() == 'y' or answer.lower() == 'yes':
        print("\nAlright, let's log you in!")
        username = input("Username: ")
        password = getpass(prompt="Password: ")

        # Validate the login credentials
        user = validate_login(username, password)
    else:
        user = None

    return user


# Create account
def create_account() -> User:
    # Prompt user for username
    username = input("Choose your username: ")

    # Check if username is not taken
    user_account = session.query(User).filter_by(name=username).first()
    while user_account is not None:
        print("\nHmm, that username is already taken. Let's try something different!")
        username = input("Choose your username: ")
        user_account = session.query(User).filter_by(name=username).first()
        # TODO: Allow the user to leave this loop

    password = getpass(prompt="Great, choose your password now: ")
    salt = os.urandom(32)  # A new salt for this user
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    user = User(name=username, salt=salt, key=key)
    session.add(user)
    session.commit()

    user_instance = session.query(User).filter_by(name=username).first()
    print("\nYou've successfully created the account!")

    return user_instance


# Validate the login credentials
def validate_login(username, password) -> User:
    wrong_credentials_message = "Wrong username or password!"
    user_instance = session.query(User).filter_by(name=username).first()

    # Wrong username
    if user_instance is None:
        print(wrong_credentials_message)
        return None

    # Retrieve user's salt and key
    salt = user_instance.salt
    key = user_instance.key
    calculated_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    # Check if the password is correct
    if key != calculated_key:
        print(wrong_credentials_message)
        return None
    else:
        return user_instance
