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


class ParentCategory(Base):
    __tablename__ = 'parent_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget_id = Column(Integer, ForeignKey("budget.id"))
    categories = relationship("Category", backref="parent_category")

    def __repr__(self):
        return f"ParentCategory {self.name}, wchodząca w skład budżetu o ID {self.budget_id}"

    # def sum_budgeted(self):
    #     sum_budgeted = session.query(
    #         func.sum(Category.budgeted_amount)
    #         .filter(Category.parent_id == self.id)
    #         ).first()[0]
    #
    #     if sum_budgeted is None:
    #         sum_budgeted = 0.0
    #
    #     return sum_budgeted

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

    def get_activity(self, month, year):
        pass

    def get_prettytable_repr(self, month, year):
        sum_budgeted = self.get_budgeted_amount(month, year)
        return [(self.id, self.name), sum_budgeted, self.sum_activity, sum_budgeted + self.sum_activity]

