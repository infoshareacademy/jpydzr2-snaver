"""Script that creates the database based on imported models

Don't forget to import the modules :-)
"""

#Import database connection
from database import engine

#import models
from models.Base import Base
from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory
from models.Category import Category
from models.Transaction import Transaction

#Create the database
Base.metadata.create_all(engine)