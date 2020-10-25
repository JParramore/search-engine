from db.services import PageService, LocationService, WordService
from db.session import get_session
from db.models import Page, Location, Word

session = get_session()
location_service = LocationService(session)
word_service = WordService(session)
page_service = PageService(session)



word_1 = word_service.find(stem="the")
word_2 = word_service.find(stem="of")
word_3 = word_service.find(stem="analysing")
words = [word_1, word_2, word_3]
page = page_service.find(url="https://willthishappen.com/us-president-2020-female")


distance = 0 
for word, next_word in zip(words, words[1:]):
    position_word = session.query(Location).filter_by(page=page, word=word).order_by(Location.position).first().position
    position_next_word = session.query(Location).filter_by(page=page, word=next_word).order_by(Location.position).first().position
    distance += abs(position_word - position_next_word)
