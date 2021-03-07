#Import database connection
from .mydatabase import engine

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


#Create default Base class
Base = declarative_base()

#Create your models here
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budgets = relationship("Budget")

    def __repr__(self):
        return "Moje imię to: '%s'" % (self.name)

class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id")) #Creates relationship between the budget and the user
    parent_categories = relationship("ParentCategory")

class ParentCategory(Base):
    __tablename__ = 'parent_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget_id = Column(Integer, ForeignKey("budget.id"))
    categories = relationship("Category")

class Category(Base):
    __tablename__ = 'parent_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budgeted_amount = Column(Numeric) #Jeśli nie chcemy miesięcy na początku, to ten atrybut jest chyba zbędny
    available_amount = Column(Numeric)
    parent_id = Column(Integer, ForeignKey("parent_category.id"))


#create tables
Base.metadata.create_all(engine)