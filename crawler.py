from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import yaml

DO_NOT_CRAWL_TYPES = set(['.pdf', '.doc', '.xls', '.ppt', '.mp3' '.m4v' '.avi' '.mpg' '.rss',
                          '.xml', '.json', '.txt', '.git', '.zip', '.md5', '.asc', '.jpg', '.gif', '.png'])

SEED_PATH = "seed.yaml"

def stream_seeds_into_queue(seed_path):

    new_urls = deque([])
    stream = open(seed_path, 'r')
    seeds = yaml.safe_load(stream)['seed-urls']

    [new_urls.append(url) for url in seeds]

    process_urls(new_urls)


# process urls one by one until we exhaust the queue
def process_urls(new_urls):

    pages = {}
    unique_urls = set()
    broken_urls = set()

    while len(new_urls):
        # move url from the queue to processed url set
        url = new_urls.popleft()
        unique_urls.add(url)
        print('Processing %s' % url)
        try:
            response = requests.get(url)
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            broken_urls.add(url)
            continue

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        pages[url] = soup.get_text()

        base_obj = extract_base(url)
        internal_urls = scrape_url_for_links(base_obj, soup)

        for i in internal_urls:
            if not i in new_urls and not i in unique_urls:
                new_urls.append(i)


def scrape_url_for_links(base, soup):

    internal_urls = set()
    external_urls = set()

    base_url = base['base_url']
    strip_base = base['strip_base']
    path = base['path']

    for link in soup.find_all('a'):
        # extract link url from the anchor

        if 'href' in link.attrs and not link.attrs['href'].startswith('mailto:') and not link.attrs['href'][-4:len(link.attrs['href'])] in DO_NOT_CRAWL_TYPES:
            anchor = link.attrs['href']
        else:
            anchor = ''

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

    return internal_urls

# extract base url to resolve relative links


def extract_base(url):
    parts = urlsplit(url)
    
    # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit
    base = '{0.netloc}'.format(parts)
    
    path = url[:url.rfind('/')+1] if '/' in parts.path else url

    return {
        'strip_base': base.replace('www.', ''),
        'base_url': '{0.scheme}://{0.netloc}'.format(parts),
        'path': path
    }