# This is a hack to import session TODO fix this
# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
import sys

sys.path.append("..")

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from session import session

from .Base import Base
from .Transaction import Transaction
from .CategoryBudget import CategoryBudget


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("parent_category.id"))
    transactions = relationship("Transaction", backref="category")
    budgeted_amounts = relationship("CategoryBudget", backref="category")

    def __repr__(self):
        # formatted_available = "{:.2f} zł".format(self.available_amount)
        # return f"id: {self.id}, name: {self.name}, available: {formatted_available}"
        return f"id: {self.id}, name: {self.name}"


    def get_transactions(self):
        return session.query(Transaction).filter(Transaction.category_id == self.id).all()

    def get_budgeted_amount(self, month, year):
        budget_for_the_month = session.query(CategoryBudget)\
            .filter(
            CategoryBudget.category_id == self.id,
            CategoryBudget.month == month,
            CategoryBudget.year == year).first()

        if not budget_for_the_month:
            return 0.00

        else:
            return budget_for_the_month.budgeted_amount

    @property
    def sum_activity(self):
        sum_activity = session.query(
            func.sum(Transaction.amount_inflow - Transaction.amount_outflow)) \
            .join(Category) \
            .filter(Category.id == self.id).first()[0]

        if sum_activity is None:
            sum_activity = 0.0

        return sum_activity

    def get_prettytable_repr(self, month, year):
        sum_budgeted = self.get_budgeted_amount(month, year)
        return [(self.id, self.name), sum_budgeted, self.sum_activity, sum_budgeted + self.sum_activity]