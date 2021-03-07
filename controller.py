#Import models
from models.Base import Base
from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory
from session import session

global_user_id = None

#Define the logic

def login():
    username = input("Hello, what's your name?\n")
    get_user(username)

def get_user(username):
    user_instance = session.query(User).filter_by(name=username).first()
    if user_instance is None:
        create_account(username)
    else:
        print("\n{}, Twoje ID w bazie danych to {}. Twój budżet to: [TODO]\n".format(user_instance.name, user_instance.id))
        show_budget()

def create_account(username):
    print("\nHi, {}, seems like you don't have an account. Worry not! We've just created one for you! :-)".format(username))
    user = User(name=username)
    session.add(user)
    session.commit()
    get_user(username)

def show_budget():
    pass
