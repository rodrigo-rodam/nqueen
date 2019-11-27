from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(autocommit=True, autoflush=False, bind=create_engine())
session = scoped_session(Session)
