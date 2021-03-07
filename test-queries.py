from database import engine
from session import session
from models.User import User
from models.Budget import Budget

#Retrive a User object with a name 'Krzysiek'
get_user = session.query(User).filter_by(name='Krzysiek').first()

#Does it work?
print(get_user)

#Show all Users in the db
for instance in session.query(User).order_by(User.id):
    print(instance)

for instance in session.query(Budget).order_by(Budget.id):
    print(instance)