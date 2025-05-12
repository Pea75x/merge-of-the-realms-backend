from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/merge_of_the_realms_db"

engine = create_engine(DATABASE_URL)
# create engine - creates connection to database, 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Sessions are used to interact with database (adding/ querying/ deleting records)

# autocommit=False
# Prevents SQLAlchemy from automatically committing changes to database (manually call db.commit() to commit transaction)

# autoflush=False
# Prevents SQLAlchemy from automatically flushing changes to database

# bind=engine
# Session is connected to engine you created above, so it knows which database to use

Base = declarative_base()
# function that returns base class for database models
# Models inherit from this Base class to interact with the database.

def get_db():
    db = SessionLocal()  # Creates a new DB session
    try:
        yield db  # Yielding it to be used by the route
    finally:
        db.close()