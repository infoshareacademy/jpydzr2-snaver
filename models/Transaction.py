import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date

from .Base import Base


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    payee_name = Column(String)
    amount_inflow = Column(Float)
    amount_outflow = Column(Float)
    category_id = Column(Integer, ForeignKey("category.id"))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    receipt_date = Column(Date)

    def __repr__(self):
        formatted_outflow = "{:.2f} zł".format(self.amount_outflow)
        return f"Transakcja o ID {self.id} na kwotę {formatted_outflow}. ID kategorii: {self.category_id}, " \
               f"data dodania pozycji: {self.created_date}, data paragonu: {self.receipt_date}"
