from db.services import PageService, LocationService, WordService
from db.session import get_session


def query(key_words):
    return [
        {
            'url': 'https://google.com/',
            'title': 'Google',
            'description': 'A description.',
            'highlight': 'Where the keywords were found.',
        },
        {
            'url': 'https://example.org/',
            'title': 'Example',
            'description': 'Another description.',
            'highlight': 'Where the keywords were found.',
        },
    ]
    key_words = key_words.split()
    session = get_session()
    page_service = PageService(session)
    location_service = LocationService(session)
    word_service = WordService(session)

    # pages_ = []
    for key_word in key_words:
        word = word_service.find(stem=key_word)
        for page in word.pages:
            num_appearances = len(
                location_service.find_all(word=word, page=page))
            print(
                f'The word "{word.stem}" has appeard {num_appearances} time(s) on {page.url}')
