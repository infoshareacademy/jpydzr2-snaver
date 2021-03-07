from models import User, Budget, Category, ParentCategory
from session import session

#W tym pliku jest definiowana logika programu

def login():
    username = input("Hello, what is your username?\n")
    get_user(username)

def get_user(username):
    user_instance = session.query(User).filter_by(name=username).first()
    print(user_instance)