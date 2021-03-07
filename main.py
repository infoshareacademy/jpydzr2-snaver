from controller import *

print(session)
print(session.query(User).filter_by(id=1).first())

login()