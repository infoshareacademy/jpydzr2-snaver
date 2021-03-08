from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
# from sqlalchemy.orm import relationship

from .Base import Base

#Create your models here
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "Moje imię to: '%s'" % (self.name)