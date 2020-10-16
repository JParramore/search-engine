from db.services import PageService, LocationService, WordService
from db.session import get_session

def query(keywords):
    session = get_session()
    page_service = PageService(session)
    location_service = LocationService(session)
    word_service = WordService(session)

    # pages = []
    # for key_word in keywords:
    #     for word in word_service.find(stem=key_word):
    #         pages.add(word.)