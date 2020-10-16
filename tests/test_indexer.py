from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from indexer import add_to_index
from db.models import Base, Page, Location, Word
import unittest
from unittest.mock import MagicMock, patch


def get_testing_session():
    engine = create_engine('sqlite:///:memory:')  # for logging, add echo=True
    target_metadata = Base.metadata
    target_metadata.create_all(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


class TestIndexerData(unittest.TestCase):
    @patch('indexer.get_session')
    def test_add_data(self, mock_get_session):
        mock_session = get_testing_session()
        mock_get_session.return_value = mock_session

        url = 'http://google.com'
        title = 'Google'
        text = 'apple banana orange apple'
        description = 'Some description.'
        add_to_index(url, title, text, description)

        page = mock_session.query(Page).first()
        words = mock_session.query(Word).all()

        # page saved
        self.assertEqual(page.url, url)
        self.assertEqual(page.title, title)
        self.assertEqual(page.description, description)

        # correct amount of locations
        self.assertEqual(len(page.locations), 4)

        # use existing words when necessary
        self.assertEqual(len(words), 3)

        # clear up stale locations
        old_locations = page.locations
        add_to_index(url, title, text, description)
        for new_location in mock_session.query(Page).first().locations:
            self.assertNotIn(new_location, old_locations)
