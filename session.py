#import engine and sessionmaker
from database import engine
from sqlalchemy.orm import sessionmaker

#create and export session
Session = sessionmaker(bind=engine)
session = Session()