from sqlalchemy.orm import sessionmaker
from mydatabase import engine
from models import User

Session = sessionmaker(bind=engine)

session = Session()

#Retrive an instance of a User object with a name 'Krzysiek'
get_user = session.query(User).filter_by(name='Krzysiek').first()

#Does it work?
print(get_user)

#Show all Users in the db
for instance in session.query(User).order_by(User.id):
    print(instance)