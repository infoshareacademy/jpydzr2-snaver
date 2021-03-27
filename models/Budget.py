from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .Base import Base


class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    parent_categories = relationship("ParentCategory", backref="budget")

    def __repr__(self):
        return f"Name: {self.name}, Id: {self.id}, Owner id: {self.user_id}"
