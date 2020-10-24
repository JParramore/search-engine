import sys
from db.models import Page, Location, Word


class ModelServiceBase:
    def __init__(self, model, session):
        self.model = model
        self.session = session

    def find(self, **kwargs):
        return self.session.query(self.model).filter_by(**kwargs).first()

    def find_all(self, **kwargs):
        return self.session.query(self.model).filter_by(**kwargs).all()

    def new(self, **kwargs):
        instance = self.model(**kwargs)
        self.session.add(instance)
        return instance

    def save(self):
        self.session.commit()


class PageService(ModelServiceBase):
    def __init__(self, session):
        ModelServiceBase.__init__(self, Page, session)


class LocationService(ModelServiceBase):
    def __init__(self, session):
        ModelServiceBase.__init__(self, Location, session)

    def clean_up(self, page):
        # TODO: can this cause dangling words?
        self.session.query(self.model).filter(
            self.model.page_id == page.id).delete()

    def words_on_page(self, words, page):
        '''
        How many combined instances of the key words are on a page?
        '''
        count = 0
        for word in words:
            count += len(
                self.session.query(self.model).filter(
                    self.model.page == page
                ).filter(self.model.word == word).all()
            )
        return count

    def highest_position_of_word(self, words, page):
        '''
        What is the highest position on a page of any of these key words?
        (0 is the highest)
        '''
        highest_position = sys.maxsize
        for word in words:
            locations = [location.position for location in
                         self.session.query(self.model).filter(
                             self.model.page == page
                         ).filter(self.model.word == word).all()]
            if locations:
                highest_position = min(locations)
        return highest_position

    def distance_between_words(self, words, page):
        '''
        What is the sum of distances between each keyword in order?
        '''
        distance = 0
        for word, next_word in zip(words, words[1:]):
            position = self.session.query(self.model).filter_by(
                page=page, word=word).order_by(self.model.position).first().position
            next_position = self.session.query(self.model).filter_by(
                page=page, word=next_word).order_by(self.model.position).first().position
            if position and next_position:
                distance += abs(position - next_position)
        return distance


class WordService(ModelServiceBase):
    def __init__(self, session):
        ModelServiceBase.__init__(self, Word, session)
