from database import engine
from session import session
from models.User import User
from models.Budget import Budget


#ADD USERS
session.add_all([
     User(name='Zbyszek'),
     User(name='Krzysiek'),
     User(name='Mariola')
     ])

#Zapisz do bazy
session.commit()

#ADD BUDGETS
budget_list = []

x = 1
for n in range(3):
     budget_list.append(Budget(name="Mój budżet", user_id=x))
     x += 1

session.add_all(budget_list)
session.commit()