from indexer import add_to_index
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from db.services import PageService, LocationService, WordService
from db.models import Word, Page, Location
from setup.session import get_testing_session


class TestServices(unittest.TestCase):
    def test_location_related_services(self):

        mock_session = get_testing_session()
        page_service = PageService(mock_session)
        word_service = WordService(mock_session)
        location_service = LocationService(mock_session)

        url = 'http://google.com'
        title = 'Google'
        text = 'feeling lucky'
        description = 'This is a description.'
        index = 0

        page = page_service.new(url=url, title=title, description=description)

        first_word = text.split()[0]
        word = word_service.new(stem=first_word)

        location = location_service.new(page=page, word=word, position=index)

        page_service.save()

        query_word = mock_session.query(
            Word).filter_by(stem=first_word).first()
        query_page = mock_session.query(Page).filter_by(url=url).first()
        query_location = mock_session.query(Location).filter_by(
            word=word, page=page, position=index).first()

        self.assertEqual(query_word.stem, first_word)
        self.assertEqual(query_page.url, url)
        self.assertEqual(query_location.word_id, word.id)
        self.assertEqual(query_location.page_id, page.id)
