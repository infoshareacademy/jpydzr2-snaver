#Import database connection
from database import engine

# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()

#Import all models
# from models import *

from models.Base import Base
from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory

#set declarative class

#Create the database
Base.metadata.create_all(engine)