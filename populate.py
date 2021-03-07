from database import engine
from session import session
from models.User import User

session.add_all([
     User(name='Zbyszek'),
     User(name='Krzysiek'),
     User(name='Mariola')
     ])

#Zapisz do bazy
session.commit()