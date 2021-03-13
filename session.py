from sqlalchemy.orm import sessionmaker

from database import engine

# create and export session
Session = sessionmaker(bind=engine)
session = Session()
