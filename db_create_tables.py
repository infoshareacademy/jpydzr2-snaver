from database import engine
from models.Base import Base
from models.Budget import Budget
from models.Category import Category
from models.CategoryBudget import CategoryBudget
from models.ParentCategory import ParentCategory
from models.Transaction import Transaction
from models.User import User


def create_db():
    Base.metadata.create_all(engine)


create_db()
