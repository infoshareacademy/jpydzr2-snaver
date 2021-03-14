from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
import datetime

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

    def __repr__(self):
        formatted_outflow = "{:.2f} zł".format(self.amount_outflow)
        return "Transakcja o ID %i na kwotę %s. ID kategorii: %i" % (self.id, formatted_outflow, self.category_id)
