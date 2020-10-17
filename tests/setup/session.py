from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from db.models import Base

def get_testing_session():
    engine = create_engine('sqlite:///:memory:')  # for logging, add echo=True
    target_metadata = Base.metadata
    target_metadata.create_all(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()