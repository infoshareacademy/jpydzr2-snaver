from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    # account_id = Column(Integer, ForeignKey)
    name = Column(String)
    payee_name = Column(String)
    # payee_date = Column(Date)
    amount_inflow = Column(Numeric)
    amount_outflow = Column(Numeric)
    # parent_id = Column(Integer, ForeignKey("category_budget.id"))