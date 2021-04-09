"""Script that creates the database based on imported models

Don't forget to import the modules :-)
"""

from database import engine
# Even "unused" models have to be imported here TODO: Fix this behaviour
from models.Base import Base
from models.Budget import Budget
from models.Category import Category
from models.CategoryBudget import CategoryBudget
from models.ParentCategory import ParentCategory
from models.Transaction import Transaction
from models.User import User


# Create the database
def create_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
