from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .Base import Base
from .Category import Category

# This is a hack to import session TODO fix this
# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
import sys

sys.path.append("..")

from session import session


class ParentCategory(Base):
    __tablename__ = 'parent_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget_id = Column(Integer, ForeignKey("budget.id"))

    def __repr__(self):
        return "ParentCategory '%s', wchodząca w skład budżetu o ID %i" % (self.name, self.budget_id)

    def get_categories(self):
        return session.query(Category).filter(Category.parent_id == self.id).all()
