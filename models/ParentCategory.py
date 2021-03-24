from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .Base import Base
from .Category import Category


class ParentCategoryNotFoundException(Exception):
    def __init__(self, category_id=None):
        if category_id:
            self.category_id = category_id
            self.message = f"Parent Category with id: {self.category_id} does not exist"
        else:
            self.message = "Parent Category does not exist"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ParentCategory(Base):
    __tablename__ = 'parent_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget_id = Column(Integer, ForeignKey("budget.id"))
    categories = relationship("Category", backref="parent_category")

    def __repr__(self):
        return f"ParentCategory {self.name}, wchodząca w skład budżetu o ID {self.budget_id}"

    def give_parent_categories(self):
        return [self.id, self.name]