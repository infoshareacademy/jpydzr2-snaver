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
from .style import style


class ParentCategory(Base):
    __tablename__ = 'parent_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget_id = Column(Integer, ForeignKey("budget.id"))
    categories = relationship("Category", backref="parent_category")

    def __repr__(self):
        return f"ParentCategory {self.name}, wchodząca w skład budżetu o ID {self.budget_id}"

    @property
    def sum_budgeted(self):
        sum_budgeted = session.query(
            func.sum(Category.budgeted_amount)
            .filter(Category.parent_id == self.id)
            ).first()[0]

        if sum_budgeted is None:
            sum_budgeted = 0.0

        return sum_budgeted

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
    def prettytable_repr(self):
        sum_available = self.sum_budgeted + self.sum_activity

        if sum_available < 0:
            sum_available = f"{style.tRED}%.2f{style.RESET}" % sum_available
        else:
            sum_available = f"{style.tGREEN}%.2f{style.RESET}" % sum_available
        # NOTE: Above '%.2f' is made for printing two decimal places including zeros at the end.

        return [(self.id, self.name), self.sum_budgeted, self.sum_activity, sum_available]