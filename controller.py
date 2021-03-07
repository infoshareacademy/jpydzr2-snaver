# import os, sys
# from pathlib import Path
# sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import sessionmaker
# from .database.mydatabase import engine as engine
from database.models import User
# from database.models import 
from database.populate import populate
from database.mydatabase import engine


Session = sessionmaker(bind=engine)

session = Session()

populate()

#W tym pliku jest definiowana logika programu

def login():
    username = input("Hello, what is your username?\n")
    get_user(username)

def get_user(username):
    user_instance = session.query(User).filter_by(name=username).first()
    print(user_instance)