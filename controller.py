#Import models
from models.Base import Base
from models.User import User
# from models.Budget import Budget
# from models.ParentCategory import ParentCategory
from session import session

#W tym pliku jest definiowana logika programu

def login():
    username = input("Hello, what is your username?\n")
    get_user(username)

def get_user(username):
    user_instance = session.query(User).filter_by(name=username).first()
    print("Cześć, {}, Twoje ID to {}".format(user_instance.name, user_instance.id))