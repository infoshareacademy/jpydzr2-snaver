from sqlalchemy import Column, Integer, String, LargeBinary

from .Base import Base


# from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    salt = Column(LargeBinary)
    key = Column(LargeBinary)

    def __repr__(self):
        return "Moje imię to %s, a moje id to %i" % (self.name, self.id)
