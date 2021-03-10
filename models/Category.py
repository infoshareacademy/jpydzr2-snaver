from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

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
    budgeted_amount = Column(Float)
    available_amount = Column(Float)
    parent_id = Column(Integer, ForeignKey("parent_category.id"))
    transactions = relationship("Transaction", backref="category")

    def __repr__(self):
        formatted_available = "{:.2f} zł".format(self.available_amount)
        return f"id: {self.id}, name: {self.name}"

    def get_transactions(self):
        return session.query(Transaction).filter(Transaction.category_id == self.id).all()
