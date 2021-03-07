from database.mydatabase import engine

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Category import Category

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class ParentCategory(Base):
    __tablename__ = 'parent_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget_id = Column(Integer, ForeignKey("budget.id"))
    categories = relationship("Category")

    def get_categories(self):
        return ParentCategory.query.filter((ParentCategory.budget_id == self.id)).all()

    @property
    def available_amount(self):
        all_categories = Category.get_categories()
        available_amount = 0
        for category in all_categories:
            available_amount += category.available_amount
        return available_amount
