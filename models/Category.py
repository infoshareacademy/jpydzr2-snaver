from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from session import session

from .Base import Base
from .Transaction import Transaction
from .CategoryBudget import CategoryBudget

from datetime import datetime
from calendar import monthrange


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("parent_category.id"))
    transactions = relationship("Transaction", backref="category")
    budgeted_amounts = relationship("CategoryBudget", backref="category")

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

    def get_activity_this_month(self, month, year):
        activity = session.query(
            func.sum(Transaction.amount_inflow - Transaction.amount_outflow)) \
            .join(Category) \
            .filter(
            Category.id == self.id,
            Transaction.receipt_date >= datetime(year, month, 1),
            Transaction.receipt_date <= datetime(year, month, monthrange(year, month)[1])).first()[0]

        if not activity:
            return 0.00
        else:
            return activity

    def get_budgeted_this_month(self, month, year):
        budget_for_the_month = session.query(CategoryBudget) \
            .filter(
            CategoryBudget.category_id == self.id,
            CategoryBudget.datetime >= datetime(year, month, 1),
            CategoryBudget.datetime <= datetime(year, month, monthrange(year, month)[1])
        ).first()

        if not budget_for_the_month:
            return 0.00

        else:
            return budget_for_the_month.budgeted_amount

    def get_available_this_month(self, month, year):
        budgeted_this_far = session.query(
            func.sum(CategoryBudget.budgeted_amount)) \
            .filter(
            CategoryBudget.category_id == self.id,
            CategoryBudget.datetime <= datetime(year, month, monthrange(year, month)[1])
        ).first()[0]

        if not budgeted_this_far:
            budgeted_this_far = 0.00

        activity_this_far = session.query(
            func.sum(Transaction.amount_outflow)) \
            .filter(
            Transaction.category_id == self.id,
            Transaction.created_date <= datetime(year, month, monthrange(year, month)[1])
        ).first()[0]

        if not activity_this_far:
            activity_this_far = 0.00

        return budgeted_this_far + activity_this_far

    def get_outflow_this_month(self, month, year):
        activity = session.query(
            func.sum(Transaction.amount_outflow)) \
            .join(Category) \
            .filter(
            Category.id == self.id,
            Transaction.receipt_date >= datetime(year, month, 1),
            Transaction.receipt_date <= datetime(year, month, monthrange(year, month)[1])
        ).first()[0]

        if not activity:
            return 0.00
        else:
            return activity

    def get_prettytable_repr(self, month, year):
        budgeted_this_month = self.get_budgeted_this_month(month, year)
        outflow_this_month = self.get_outflow_this_month(month, year)
        available_this_month = self.get_available_this_month(month, year)
        # available_up_to_this_point = budgeted_this_month - outflow_this_month
        return [(self.id, self.name), budgeted_this_month, outflow_this_month, available_this_month]
