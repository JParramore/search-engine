from db.services import PageService, LocationService, WordService
from db.session import get_session


def add(url, title, text, description):
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
        # we've seen this page before, keep it up to date by:
        # removing its locations
        location_service.clean_up(existing_page)
        location_service.save()
        page = existing_page
    else:
        page = page_service.new(url=url, title=title, description=description)

    for index, stem in enumerate(text.split()):
        word = word_service.find(stem=stem)
        if not word:
            word = word_service.new(stem=stem)
        location = location_service.new(position=index)
        word.locations.append(location)
        page.locations.append(location)
    word_service.save()
    location_service.save()
    page_service.save()
