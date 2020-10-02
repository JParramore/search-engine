from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import yaml

class Page:
  def __init__(self, url, text):
    self.url = url
    self.text = text

new_urls = deque([])

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

    # load urls from seed file
    stream = open("seed.yaml", 'r')
    seeds = yaml.safe_load(stream)['seed-urls']

    # queue all seed urls
    [ new_urls.append(url) for url in seeds ]

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

        base_obj = extract_base(url)
        scrape_url_for_links(base_obj, response)

        for i in internal_urls:
            if not i in new_urls and not i in unique_urls:
                new_urls.append(i)

def scrape_url_for_links(base, response):
    
    soup = BeautifulSoup(response.text, 'lxml')

    #print(soup.get_text()) # print the page's text too

    base_url=base['base_url']
    strip_base=base['strip_base']
    path=base['path']

    for link in soup.find_all('a'): 
    
        # extract link url from the anchor
        anchor = link.attrs['href'] if 'href' in link.attrs else ''
        if anchor.startswith('/'):
            local_link = base_url + anchor
            internal_urls.add(local_link)
        elif strip_base in anchor:
            internal_urls.add(anchor)
        elif not anchor.startswith('http'):
            local_link = path + anchor
            internal_urls.add(local_link)
        else:
            external_urls.add(anchor)

# extract base url to resolve relative links
def extract_base(url):
    parts = urlsplit(url)
    base = '{0.netloc}'.format(parts) # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit
    return {
            'strip_base' : base.replace('www.', ''),
            'base_url' : '{0.scheme}://{0.netloc}'.format(parts), 
            'path' : url[:url.rfind('/')+1] if '/' in parts.path else url
            }

process_urls()