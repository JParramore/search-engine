from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from indexer import add_to_index
from db.models import Base, Page, Location, Word
import unittest
from unittest.mock import MagicMock, patch
from setup.session import get_testing_session

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
        locations = mock_session.query(Location).filter_by(page_id = page.id).all()
        self.assertEqual(len(locations), 4)

        # use existing words when necessary
        self.assertEqual(len(words), 3)

        # clear up stale locations
        old_locations = locations
        add_to_index(url, title, text, description)
        locations = mock_session.query(Location).filter_by(page_id = page.id).all()
        for new_location in locations:
            self.assertNotIn(new_location, old_locations)
