from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime

from Base import Base


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    payee_name = Column(String)
    amount_inflow = Column(Numeric)
    amount_outflow = Column(Numeric)
    category_id = Column(Integer, ForeignKey("category.id"))
    date = Column(DateTime)

    def __repr__(self):
        formatted_outflow = "{:.2f} zł".format(self.amount_outflow)
        return "Transakcja o ID %i na kwotę %s. ID kategorii: %i" % (self.id, formatted_outflow, self.category_id)
