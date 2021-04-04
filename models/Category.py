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
        formatted_available = "{:.2f} zł".format(self.available_amount)
        return f"id: {self.id}, name: {self.name}, available: {formatted_available}"

    def get_transactions(self):
        return session.query(Transaction).filter(Transaction.category_id == self.id).all()

    def get_budgeted_amount(self, month, year):
        budgeted_amount = session.query(CategoryBudget)\
            .filter(
            CategoryBudget.category_id == self.id,
            CategoryBudget.month == month,
            CategoryBudget.year == year).first()

        if not budgeted_amount:
            budgeted_amount = 0.00

        return budgeted_amount

    @property
    def available_amount(self): #TODO - do przepisania
        amount = (session.query(func.sum(Transaction.amount_outflow - Transaction.amount_inflow))
                  .filter(Transaction.category_id == self.id).first())[0]
        if amount:
            return self.__budgeted_amount - float(amount)
        else:
            return self.__budgeted_amount

    @property
    def prettytable_repr(self, month, year):
        self.activity_amount = self.get_budgeted_amount(month, year) - self.available_amount
        return [(self.id, self.name), self.get_budgeted_amount(month, year), - self.activity_amount, self.available_amount]
