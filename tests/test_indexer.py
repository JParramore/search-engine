from sqlalchemy.orm import session
from indexer import add
import unittest
from unittest.mock import MagicMock, patch, call


class TestIndexer(unittest.TestCase):
    @patch('indexer.PageService')
    @patch('indexer.LocationService')
    @patch('indexer.WordService')
    @patch('indexer.get_session')
    def test_add_normal_flow(self, mock_get_session, mock_word_service, mock_location_service, mock_page_service):
        url = 'http://google.com'
        title = 'Google'
        text = 'apple banana orange'
        add(url, title, text)

        # do we look for an existing page
        mock_page_service.return_value.find.assert_any_call(url=url)

        # do we process each word
        mock_word_service.return_value.find.assert_any_call(stem='apple')
        mock_word_service.return_value.find.assert_any_call(stem='banana')
        mock_word_service.return_value.find.assert_any_call(stem='orange')

        # do we create each location
        mock_location_service.return_value.new.assert_any_call(position=0)
        mock_location_service.return_value.new.assert_any_call(position=1)
        mock_location_service.return_value.new.assert_any_call(position=2)

        # do we append these locations
        mock_word_service.return_value.find.return_value.locations.append.assert_any_call(
            mock_location_service.return_value.new.return_value)
        mock_page_service.return_value.find.return_value.locations.append.assert_any_call(
            mock_location_service.return_value.new.return_value)

        # do we save everything
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

        # when the page already exists, do we use the existing instance
        mock_page_service.return_value.new.assert_not_called()

        # when the page already exists, do we clean up existing locations
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

        # when all the words exists, do we use them instead of creating new ones
        mock_word_service.return_value.new.assert_not_called()
