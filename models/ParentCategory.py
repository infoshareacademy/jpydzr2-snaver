from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import relationship

from session import session

from .Base import Base
from .Category import Category
from .Transaction import Transaction
from .CategoryBudget import CategoryBudget

from calendar import monthrange
from datetime import datetime


class ParentCategory(Base):
    __tablename__ = 'parent_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget_id = Column(Integer, ForeignKey("budget.id"))
    categories = relationship("Category", backref="parent_category")

    def __repr__(self):
        return f"ParentCategory {self.name}, wchodząca w skład budżetu o ID {self.budget_id}"

    def get_activity_this_month(self, month, year):
        activity = session.query(
            func.sum(Transaction.amount_inflow - Transaction.amount_outflow)) \
            .join(Category) \
            .join(ParentCategory) \
            .filter(
            ParentCategory.id == self.id,
            Transaction.receipt_date >= datetime(year, month, 1),
            Transaction.receipt_date <= datetime(year, month, monthrange(year, month)[1])).first()[0]

        if not activity:
            return 0.00
        else:
            return activity

    def get_budgeted_this_month(self, month, year):
        budget_for_the_month = session.query(
            func.sum(CategoryBudget.budgeted_amount)) \
            .join(Category) \
            .filter(
            Category.parent_id == self.id,
            CategoryBudget.datetime >= datetime(year, month, 1),
            CategoryBudget.datetime <= datetime(year, month, monthrange(year, month)[1])).first()[0]

        if not budget_for_the_month:
            return 0.00

        else:
            return budget_for_the_month

    def get_available_this_month(self, month, year):
        budgeted_this_far = session.query(
            func.sum(CategoryBudget.budgeted_amount)) \
            .join(Category) \
            .filter(
            Category.parent_id == self.id,
            CategoryBudget.datetime <= datetime(year, month, monthrange(year, month)[1])
        ).first()[0]

        if not budgeted_this_far:
            budgeted_this_far = 0.00

        activity_this_far = session.query(
            func.sum(Transaction.amount_outflow)) \
            .join(Category) \
            .filter(
            Category.parent_id == self.id,
            Transaction.created_date <= datetime(year, month, monthrange(year, month)[1])
        ).first()[0]

        if not activity_this_far:
            activity_this_far = 0.00

        return budgeted_this_far + activity_this_far

    def get_outflow_this_month(self, month, year):
        activity = session.query(
            func.sum(Transaction.amount_outflow)) \
            .join(Category) \
            .join(ParentCategory) \
            .filter(
            ParentCategory.id == self.id,
            Transaction.receipt_date >= datetime(year, month, 1),
            Transaction.receipt_date <= datetime(year, month, monthrange(year, month)[1])).first()[0]

        if not activity:
            return 0.00
        else:
            return activity

    def get_prettytable_repr(self, month, year):
        budgeted_this_month = self.get_budgeted_this_month(month, year)
        outflow_this_month = self.get_outflow_this_month(month, year)
        available_this_month = self.get_available_this_month(month, year)
        return [[self.id, self.name.upper()], budgeted_this_month, outflow_this_month, available_this_month]
