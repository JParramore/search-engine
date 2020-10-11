from crawler import extract_base, process_urls, scrape_url_for_links, stream_seeds_into_queue
import unittest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from collections import deque


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
        html_doc = open('tests/data/test.html', 'r', encoding='utf-8').read()
        soup = BeautifulSoup(html_doc, 'lxml')
        base = extract_base(url)

        actual_internal_urls = scrape_url_for_links(base, soup)

        expected_internal_urls = set()
        expected_internal_urls.add('http://www.testcase.com/good-site-path')
        expected_internal_urls.add('https://www.testcase.com/good-site-path2')
        expected_internal_urls.add('https://www.testcase.com/goodpath3')
        expected_internal_urls.add('https://www.testcase.com/')

        self.assertCountEqual(actual_internal_urls, expected_internal_urls)

    @patch('crawler.process_urls')
    def test_stream_seeds_into_queue(self,mock_process_urls):
        
        test_yaml = 'tests/data/test.yaml'
        test_yaml_urls = deque(['https://facebook.com','https://google.com','https://www.test.com'])
        stream_seeds_into_queue(test_yaml)
        mock_process_urls.assert_called_with(test_yaml_urls)