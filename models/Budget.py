from database.mydatabase import engine

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ParentCategory import ParentCategory

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    parent_categories = relationship("ParentCategory")

    def get_parent_categories(self):
        return ParentCategory.query.filter((ParentCategory.budget_id == self.id)).all()

    @property
    def available_amount(self):
        all_parent_categories = Budget.get_parent_categories()
        available_amount = 0
        for parent_category in all_parent_categories:
            available_amount += parent_category.available_amount
        return available_amount
