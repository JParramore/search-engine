from crawler import extract_base, process_website, scrape_url_for_links, stream_seeds_into_queue
import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
from collections import deque


class DotDict(dict):
    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise AttributeError

    def __setattr__(self, key, value):
        if key in self:
            self[key] = value
            return
        raise AttributeError


class TestCrawlerMethods(unittest.TestCase):
    def test_extract_base_url(self):
        url = 'https://www.duolingo.com/'

        expected = {
            'strip_base': 'duolingo.com',
            'base_url': 'https://www.duolingo.com',
            'path': 'https://www.duolingo.com/'
        }

        actual = extract_base(url)

        self.assertEqual(actual['strip_base'], expected['strip_base'])
        self.assertEqual(actual['base_url'], expected['base_url'])
        self.assertEqual(actual['path'], expected['path'])

    def test_scrape_url_for_links(self):
        url = 'https://www.testcase.com/'
        with open('tests/data/test.html', 'r', encoding='utf-8') as stream:
            html_doc = stream.read()
        soup = BeautifulSoup(html_doc, 'lxml')
        base = extract_base(url)

        actual_internal_urls = scrape_url_for_links(base, soup)

        expected_internal_urls = set()
        expected_internal_urls.add('http://www.testcase.com/good-site-path')
        expected_internal_urls.add('https://www.testcase.com/good-site-path2')
        expected_internal_urls.add('https://www.testcase.com/goodpath3')
        expected_internal_urls.add('https://www.testcase.com/')

        self.assertCountEqual(actual_internal_urls, expected_internal_urls)

    @patch('crawler.process_website')
    def test_stream_seeds_into_queue(self, mock_process_website):
        test_yaml = 'tests/data/test.yaml'
        test_yaml_urls = ['https://facebook.com',
                          'https://google.com',
                          'https://www.test.com']
        stream_seeds_into_queue(test_yaml)
        for test_url in test_yaml_urls:
            mock_process_website.assert_any_call(test_url)

    @patch('crawler.requests')
    @patch('crawler.add_to_index')
    def test_process_website(self, add_to_index, mock_requests):
        test_url = 'https://example.org'
        mock_requests.get.return_value = DotDict({"text": "<html></html>"})
        process_website(test_url)
        mock_requests.get.assert_called_once_with('https://example.org')
