from sqlalchemy import create_engine

##connect to the sqlite database
engine = create_engine('sqlite:///foo.db')