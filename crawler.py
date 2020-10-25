from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
import yaml
from indexer import add_to_index

DO_NOT_CRAWL_TYPES = set(['.pdf', '.doc', '.xls', '.ppt', '.mp3', '.m4v',
                          '.avi', '.mpg', '.rss', '.xml', '.json', '.txt',
                          '.git', '.zip', '.md5', '.asc', '.jpg', '.gif',
                          '.png'])

SEED_PATH = "seed.yaml"
MAX_REQUESTS = 10


def stream_seeds_into_queue(seed_path):
    with open(seed_path, 'r') as stream:
        for seed_url in yaml.safe_load(stream)['seed-urls']:
            process_website(seed_url)


def process_website(start_url):
    urls = [start_url]
    visited_urls = set()

    count = 0
    while len(urls):
        count += 1
        if count > MAX_REQUESTS:
            break

        url = urls.pop()
        visited_urls.add(url)
        print(f'Processing: {url}')
        try:
            response = requests.get(url)
            if response.status_code >= 400:
                continue
        except Exception as e:
            print(f'Request error for {url} - {e}')
            continue

        soup = BeautifulSoup(response.text, 'lxml')

        add_to_index(url, get_title(soup), soup.get_text(),
                     get_description(soup))
        base_obj = extract_base(url)

        for url in scrape_url_for_links(base_obj, soup):
            if not url in urls and not url in visited_urls:
                urls.append(url)


def get_title(soup):
    if soup.title:
        return soup.title.text
    return 'This page has no title.'


def get_description(soup):
    description = 'This page has no description.'

    meta_description = soup.find('meta', attrs={"name": "description"})
    if meta_description and 'content' in meta_description.attrs:
        description = meta_description.attrs['content']

    meta_og_description = soup.find('meta', attrs={"name": "og:description"})
    if meta_og_description and 'content' in meta_og_description.attrs:
        description = meta_og_description.attrs['content']

    return description


def scrape_url_for_links(base, soup):
    internal_urls = set()
    external_urls = set()

    base_url = base['base_url']
    strip_base = base['strip_base']
    path = base['path']

    for link in soup.find_all('a'):
        if 'href' in link.attrs and not link.attrs['href'].startswith('mailto:') and not link.attrs['href'][-4:len(link.attrs['href'])] in DO_NOT_CRAWL_TYPES:
            anchor = link.attrs['href'].split('#')[0]
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


if __name__ == '__main__':
    stream_seeds_into_queue(SEED_PATH)
