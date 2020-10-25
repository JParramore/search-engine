import asyncio
from db.services import PageService, LocationService, WordService
from db.session import get_session


# https://stackoverflow.com/a/53256058
# allow functions to be 'fired and forgotten'
def background(f):
    from functools import wraps

    @wraps(f)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        if callable(f):
            return loop.run_in_executor(None, f, *args, **kwargs)
        else:
            raise TypeError('Task must be a callable')
    return wrapped


@background
def add_to_index(url, title, text, description):
    '''
    Add a page to our index. Add any new words as well as their locations
    on the page. If the page already exists in our index, presume it is stale.
    '''
    session = get_session()
    page_service = PageService(session)
    location_service = LocationService(session)
    word_service = WordService(session)

    existing_page = page_service.find(url=url)
    if existing_page:
        # seen this page before? keep it up to date by removing its locations
        location_service.clean_up(existing_page)
        location_service.save()
        page = existing_page
    else:
        page = page_service.new(url=url, title=title, description=description)

    for index, stem in enumerate(text.lower().split()):
        word = word_service.find(stem=stem)
        if not word:
            word = word_service.new(stem=stem)
        location_service.new(page=page, word=word, position=index)
    page_service.save()
    session.close()
