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
from .CategoryBudget import CategoryBudget

from session import session

class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    parent_categories = relationship("ParentCategory", backref="budget")

    def __repr__(self):
        return f"Name: {self.name}, Id: {self.id}, Owner id: {self.user_id}"

    # @property
    # def total_budgeted(self):
        # total_budgeted = session.query(
        #     func.sum(Category.budgeted_amount)) \
        #     .join(ParentCategory) \
        #     .join(Budget) \
        #     .filter(Budget.id == self.id).first()[0]
        #
        # if total_budgeted is None:
        #     total_budgeted = 0.0
        #
        # return total_budgeted

    def get_budgeted_amount(self, month, year):
        budget_for_the_month = session.query(
            func.sum(CategoryBudget.budgeted_amount)) \
            .join(Category) \
            .join(ParentCategory) \
            .filter(
            ParentCategory.budget_id == self.id,
            CategoryBudget.month == month,
            CategoryBudget.year == year).first()[0]

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
