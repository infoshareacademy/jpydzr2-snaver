from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .Base import Base
from .ParentCategory import ParentCategory


class BudgetNotFoundException(Exception):
    def __init__(self, budget_id=None):
        if budget_id:
            self.budget_id = budget_id
            self.message = f"Budget with id: {self.budget_id} does not exist"
        else:
            self.message = "Budget does not exist"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))  # Creates relationship between the budget and the user
    parent_categories = relationship("ParentCategory", backref="budget")

    def __repr__(self):
        return "Nazwa: '%s', ID właściciela: %i" % (self.name, self.user_id)
