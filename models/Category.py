# This is a hack to import session TODO fix this
# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
import sys

sys.path.append("..")

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from session import session

from .Base import Base
from .Transaction import Transaction
from styles.style import style


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    __budgeted_amount = Column("budgeted_amount", Float)
    parent_id = Column(Integer, ForeignKey("parent_category.id"))
    transactions = relationship("Transaction", backref="category")

    def __repr__(self):
        formatted_available = "{:.2f} zł".format(self.available_amount)
        return f"id: {self.id}, name: {self.name}, available: {formatted_available}"

    def get_transactions(self):
        return session.query(Transaction).filter(Transaction.category_id == self.id).all()

    @property
    def available_amount(self):
        amount = (session.query(func.sum(Transaction.amount_outflow - Transaction.amount_inflow))
                  .filter(Transaction.category_id == self.id).first())[0]
        if amount:
            return self.__budgeted_amount - float(amount)
        else:
            return self.__budgeted_amount

    @hybrid_property
    def budgeted_amount(self):
        return self.__budgeted_amount

    @budgeted_amount.setter
    def budgeted_amount(self, amount):
        self.__budgeted_amount = amount
        session.query(Category).filter_by(id=self.id).update({'budgeted_amount': amount})
        session.commit()

    @property
    def prettytable_repr(self):
        self.activity_amount = self.budgeted_amount - self.available_amount

        if self.available_amount == 0:
            category = f"{style.tBLUE}({self.id}) {self.name}{style.RESET}"
            available_amount = f"{style.tBLUE}%.2f{style.RESET}" % self.available_amount
        elif self.available_amount < 0:
            category = f"{style.tRED}({self.id}) {self.name}{style.RESET}"
            available_amount = f"{style.tRED}%.2f{style.RESET}" % self.available_amount
        else:
            category = f"{style.tGREEN}({self.id}) {self.name}{style.RESET}"
            available_amount = f"{style.tGREEN}%.2f{style.RESET}" % self.available_amount
        # NOTE: Above '%.2f' is made for printing two decimal places including zeros at the end.

        return [category, self.budgeted_amount, -(self.activity_amount), available_amount]