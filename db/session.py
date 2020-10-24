from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def get_session():
    from config import db
    engine = create_engine(db) # for verbose: echo=True
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    return Session()
