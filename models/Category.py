from database.mydatabase import engine

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from Transaction import Transaction

Base = declarative_base()


class Category(Base):
    __tablename__ = 'parent_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budgeted_amount = Column(Numeric)  # Jeśli nie chcemy miesięcy na początku, to ten atrybut jest chyba zbędny
    available_amount = Column(Numeric)
    parent_id = Column(Integer, ForeignKey("parent_category.id"))

    def get_transactions(self):
        return Transaction.query.filter((Transaction.category_id == self.id)).all()

    @property
    def available_amount(self):
        all_transactions = Transaction.get_transactions()
        available_amount = 0
        for transaction in all_transactions:
            available_amount += transaction.inflow
            available_amount += transaction.outflow
        return available_amount
