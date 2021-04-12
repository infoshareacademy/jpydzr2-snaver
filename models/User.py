from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .Base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    salt = Column(LargeBinary)
    key = Column(LargeBinary)
    budgets = relationship("Budget", backref="user")

    def __repr__(self):
        return "Moje imię to %s, a moje id to %i" % (self.name, self.id)
