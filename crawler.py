from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import yaml


# root urls
url = ['https://scrapethissite.com']

new_urls = deque([url])

# processed urls
unique_urls = set()

# internal urls
internal_urls = set()

# external urls
external_urls = set()

# broken urls
broken_urls = set()

# process urls one by one until we exhaust the queue
def process_urls():

    while len(new_urls):
        # move url from the queue to processed url set
        url = new_urls.popleft()
        unique_urls.add(url)
        # print the current url
        print('Processing %s' % url)
        try:
            response = requests.get(url)
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):    
            # add broken urls to it’s own set, then continue
            broken_urls.add(url)
            continue



process_urls()