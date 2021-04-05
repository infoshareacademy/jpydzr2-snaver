from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship
from sqlalchemy import func

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

    def get_activity_for_the_month(self, month, year):
        activity = session.query(
            func.sum(Transaction.amount_inflow - Transaction.amount_outflow)) \
            .join(Category) \
            .join(ParentCategory) \
            .filter(
            ParentCategory.id == self.id,
            Transaction.created_date >= datetime(year, month, monthrange(year, month)[0]),
            Transaction.created_date <= datetime(year, month + 2, monthrange(year, month)[1])).first()[0]

        if not activity:
            return 0.00
        else:
            return activity

    def get_budgeted_amount(self, month, year):
        budget_for_the_month = session.query(
            func.sum(CategoryBudget.budgeted_amount)) \
            .join(Category) \
            .filter(
            Category.parent_id == self.id,
            CategoryBudget.month == month,
            CategoryBudget.year == year).first()[0]

        if not budget_for_the_month:
            return 0.00

        else:
            return budget_for_the_month

    @property
    def sum_activity(self):
        sum_activity = session.query(
            func.sum(Transaction.amount_inflow - Transaction.amount_outflow)) \
            .join(Category).join(ParentCategory) \
            .filter(ParentCategory.id == self.id).first()[0]

        if sum_activity is None:
            sum_activity = 0.0

        return sum_activity

    @property
    def available(self):
        budgeted = session.query(
            func.sum(CategoryBudget.budgeted_amount)) \
            .join(Category) \
            .filter(
            Category.parent_id == self.id).first()[0]

        return budgeted - self.sum_activity

    def get_prettytable_repr(self, month, year):
        budgeted_this_month = self.get_budgeted_amount(month, year)
        activity = self.get_activity_for_the_month(month, year)
        return [(self.id, self.name), budgeted_this_month, activity, self.available]

