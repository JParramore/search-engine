from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


def get_session():
    from config import db
    engine = create_engine(db, echo=True)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()
