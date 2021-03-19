from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .Base import Base
from .ParentCategory import ParentCategory

class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))  # Creates relationship between the budget and the user
    parent_categories = relationship("ParentCategory", backref="budget")

    def __repr__(self):
        return "Nazwa: '%s', ID właściciela: %i" % (self.name, self.user_id)

    def give_budgets(self):
        return [self.id, self.name, self.user_id]