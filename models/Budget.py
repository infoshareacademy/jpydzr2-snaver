from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import relationship

from session import session

from .Base import Base
from .Category import Category
from .ParentCategory import ParentCategory
from .Transaction import Transaction
from .CategoryBudget import CategoryBudget

from datetime import datetime
from calendar import monthrange


class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    parent_categories = relationship("ParentCategory", backref="budget")

    def __repr__(self):
        return f"Name: {self.name}, Id: {self.id}, Owner id: {self.user_id}"

    def get_budgeted_this_month(self, month, year):
        budget_for_the_month = session.query(
            func.sum(CategoryBudget.budgeted_amount)) \
            .join(Category) \
            .join(ParentCategory) \
            .filter(
            ParentCategory.budget_id == self.id,
            CategoryBudget.datetime >= datetime(year, month, 1),
            CategoryBudget.datetime <= datetime(year, month, monthrange(year, month)[1])
            ).first()[0]

        if not budget_for_the_month:
            return 0.00

        else:
            return budget_for_the_month

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

    def get_activity_this_month(self, month, year):
        total_activity = session.query(
            func.sum(Transaction.amount_inflow - Transaction.amount_outflow)) \
            .join(Category) \
            .join(ParentCategory) \
            .filter(
            ParentCategory.budget_id == self.id,
            Transaction.created_date >= datetime(year, month, 1),
            Transaction.created_date <= datetime(year, month, monthrange(year, month)[1])
            ).first()[0]

        if total_activity is None:
            total_activity = 0.0

        return total_activity

    def get_available_this_month(self, month, year):
        budgeted_this_far = session.query(
            func.sum(CategoryBudget.budgeted_amount)) \
            .join(Category) \
            .join(ParentCategory) \
            .filter(
            ParentCategory.budget_id == self.id,
            CategoryBudget.datetime <= datetime(year, month, monthrange(year, month)[1])
            ).first()[0]

        if not budgeted_this_far:
            budgeted_this_far = 0.00

        return budgeted_this_far + self.total_activity

    def all_transactions(self):
        transactions = session.query(Transaction).join(Category).join(ParentCategory) \
            .join(Budget) \
            .filter(Budget.id == self.id).all()
        return transactions

    @property
    def total_inflow(self):
        total_inflow = session.query(
            func.sum(Transaction.amount_inflow)) \
            .join(Category).join(ParentCategory) \
            .join(Budget) \
            .filter(Budget.id == self.id).first()[0]

        if total_inflow is None:
            total_inflow = 0.0

        return total_inflow

    @property
    def total_outflow(self):
        outflow = session.query(
            func.sum(Transaction.amount_outflow)) \
            .join(Category).join(ParentCategory) \
            .join(Budget) \
            .filter(Budget.id == self.id).first()[0]

        if outflow is None:
            outflow = 0.0

        return outflow