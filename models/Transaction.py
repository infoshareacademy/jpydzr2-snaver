from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    payee_name = Column(String)
    amount_inflow = Column(Numeric)
    amount_outflow = Column(Numeric)
    category_id = Column(Integer, ForeignKey("category.id"))
    payee_date = Column(Date)