"""Script that creates the database based on imported models

Don't forget to import the modules :-)
"""

from database import engine

# Even "unused" models have to be imported here TODO: Fix this behaviour
from models.Base import Base
from models.User import User
from models.Budget import Budget
from models.ParentCategory import ParentCategory
from models.Category import Category
from models.Transaction import Transaction

# Create the database
Base.metadata.create_all(engine)
