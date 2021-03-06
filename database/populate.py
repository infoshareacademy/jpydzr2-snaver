from mydatabase import engine
from models import User

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()

#Add multiple Users to database
session.add_all([
     User(name='Zbyszek'),
     User(name='Krzysiek'),
     User(name='Mariola')
     ])

#Zapisz do bazy
session.commit()