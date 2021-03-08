from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
# from sqlalchemy.orm import relationship

from .Base import Base


class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id")) #Creates relationship between the budget and the user

    def __repr__(self):
        return "Budżet '%s', ID właściciela: '%i'" % (self.name, self.user_id)