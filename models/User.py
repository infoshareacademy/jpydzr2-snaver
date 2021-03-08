from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship

from .Base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "Moje imię to %s, a moje id to %i" % (self.name, self.id)
