from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy import func

from .Base import Base
from .ParentCategory import ParentCategory
from .Category import Category
from .Transaction import Transaction

from session import session


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
    user_id = Column(Integer, ForeignKey("user.id"))
    parent_categories = relationship("ParentCategory", backref="budget")

    def __repr__(self):
        return f"Name: {self.name}, Id: {self.id}, Owner id: {self.user_id}"

    @property
    def total_budgeted(self):
        total_budgeted = session.query(
            func.sum(Category.budgeted_amount)) \
            .join(ParentCategory) \
            .filter(ParentCategory.id == self.id).first()[0]

        if total_budgeted is None:
            total_budgeted = 0.0

        return total_budgeted

    @property
    def total_activity(self):
        total_activity = session.query(
            func.sum(Transaction.amount_inflow - Transaction.amount_outflow)) \
            .join(Category).join(ParentCategory) \
            .join(Budget) \
            .filter(Budget.id == self.id).first()[0]

        if total_activity is None:
            total_activity = 0.0

        return total_activity
