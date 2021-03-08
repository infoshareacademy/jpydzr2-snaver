from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship

from .Base import Base


class ParentCategory(Base):
    __tablename__ = 'parent_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget_id = Column(Integer, ForeignKey("budget.id"))

    def __repr__(self):
        return "ParentCategory '%s', wchodząca w skład budżetu o ID %i" % (self.name, self.budget_id)
