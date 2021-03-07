from sqlalchemy import create_engine

##connect to the sqlite database (or create it)
engine = create_engine('sqlite:///database/foo.db')