from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


def get_session():
    from config import db
    # for verbose: echo=True
    engine = create_engine(db)
    Session = sessionmaker(bind=engine)
    return Session()
