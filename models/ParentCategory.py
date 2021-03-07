from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from .Base import Base


class ParentCategory(Base):
    __tablename__ = 'parent_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget_id = Column(Integer, ForeignKey("budget.id"))

    def __repr__(self):
        return "ParentCategory o nazwie: '%s', w ramach budżetu o ID '%i'" % (self.name, self.budget_id)
