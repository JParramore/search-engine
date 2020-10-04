from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from indexer import add
from db.models import Base, Page, Location, Word
import unittest
from unittest.mock import MagicMock, patch, call


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
        add(url, title, text)

        page = mock_session.query(Page).first()
        words = mock_session.query(Word).all()

        # page saved
        self.assertEqual(page.url, url)
        self.assertEqual(page.title, title)

        # correct amount of locations
        self.assertEqual(len(page.locations), 4)

        # use existing words when necessary
        self.assertEqual(len(words), 3)

        # clear up stale locations
        old_locations = page.locations
        add(url, title, text)
        for new_location in mock_session.query(Page).first().locations:
            self.assertNotIn(new_location, old_locations)


class TestIndexerServices(unittest.TestCase):
    @patch('indexer.PageService')
    @patch('indexer.LocationService')
    @patch('indexer.WordService')
    @patch('indexer.get_session')
    def test_add_normal_flow(self, mock_get_session, mock_word_service, mock_location_service, mock_page_service):
        url = 'http://google.com'
        title = 'Google'
        text = 'apple banana orange'
        add(url, title, text)

        # look for an existing page
        mock_page_service.return_value.find.assert_any_call(url=url)

        # process each word
        mock_word_service.return_value.find.assert_any_call(stem='apple')
        mock_word_service.return_value.find.assert_any_call(stem='banana')
        mock_word_service.return_value.find.assert_any_call(stem='orange')

        # create each location
        mock_location_service.return_value.new.assert_any_call(position=0)
        mock_location_service.return_value.new.assert_any_call(position=1)
        mock_location_service.return_value.new.assert_any_call(position=2)

        # append these locations
        mock_word_service.return_value.find.return_value.locations.append.assert_any_call(
            mock_location_service.return_value.new.return_value)
        mock_page_service.return_value.find.return_value.locations.append.assert_any_call(
            mock_location_service.return_value.new.return_value)

        # save everything
        mock_page_service.return_value.save.assert_any_call()
        mock_location_service.return_value.save.assert_any_call()
        mock_word_service.return_value.save.assert_any_call()

    @patch('indexer.PageService')
    @patch('indexer.LocationService')
    @patch('indexer.WordService')
    @patch('indexer.get_session')
    def test_add_page_exists(self, mock_get_session, mock_word_service, mock_location_service, mock_page_service):
        mock_page = MagicMock()
        mock_page_service.return_value.find = MagicMock(return_value=mock_page)

        url = 'http://google.com'
        title = 'Google'
        text = ''
        add(url, title, text)

        # when the page already exists, use the existing instance
        mock_page_service.return_value.new.assert_not_called()

        # when the page already exists, clean up existing locations
        mock_location_service.return_value.clean_up.assert_any_call(mock_page)

    @patch('indexer.PageService')
    @patch('indexer.LocationService')
    @patch('indexer.WordService')
    @patch('indexer.get_session')
    def test_add_words_exists(self, mock_get_session, mock_word_service, mock_location_service, mock_page_service):
        mock_word = MagicMock()
        mock_word_service.return_value.find = MagicMock(mock_word)

        url = 'http://google.com'
        title = 'Google'
        text = 'apple banana orange'
        add(url, title, text)

        # when all the words exist, use them instead of creating new ones
        mock_word_service.return_value.new.assert_not_called()
