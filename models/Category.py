from sqlalchemy import Column, Integer, String, ForeignKey, Numeric

from Base import Base


# from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    budgeted_amount = Column(Numeric)  # Jeśli nie chcemy miesięcy na początku, to ten atrybut jest chyba zbędny
    available_amount = Column(Numeric)
    parent_id = Column(Integer, ForeignKey("parent_category.id"))

    def __repr__(self):
        formatted_available = "{:.2f} zł".format(self.available_amount)
        return "Kategoria '%s',  dostępna kwota: %s, ID rodzica: %i" % (self.name, formatted_available, self.parent_id)
