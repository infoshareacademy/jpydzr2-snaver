from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import String
import datetime

from session import session

from .Base import Base


class CategoryBudget(Base):
    __tablename__ = 'category_budget'

    id = Column(Integer, primary_key=True)
    __budgeted_amount = Column("budgeted_amount", Float)
    category_id = Column(Integer, ForeignKey("category.id"))
    datetime = Column(DateTime)

    def __repr__(self):
        return f"Budżet kategorii {self.category_id} na miesiąć {self.datetime.month} i rok: {self.datetime.year}"

    @hybrid_property
    def budgeted_amount(self):
        return self.__budgeted_amount

    @budgeted_amount.setter
    def budgeted_amount(self, amount):
        self.__budgeted_amount = amount
        session.query(CategoryBudget).filter_by(id=self.id).update({'budgeted_amount': amount})
        session.commit()
