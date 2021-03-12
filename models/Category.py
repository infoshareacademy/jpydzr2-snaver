from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

# This is a hack to import session TODO fix this
# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
import sys

sys.path.append("..")

from .Base import Base
from .Transaction import Transaction
from session import session


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
        amount = session.query(func.sum(Transaction.amount_outflow)).filter(Transaction.category_id == self.id).first()
        return self.__budgeted_amount - float(amount[0])

    @hybrid_property
    def budgeted_amount(self):
        return self.__budgeted_amount

    @budgeted_amount.setter
    def budgeted_amount(self, amount):
        self.__budgeted_amount = amount
        session.query(Category).filter_by(id=self.id).update({'budgeted_amount': amount})
        session.commit()
