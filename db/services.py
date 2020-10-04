from db.models import Page, Location, Word


class ModelServiceBase:
    def __init__(self, model, session):
        self.model = model
        self.session = session

    def find(self, **kwargs):
        return self.session.query(self.model).filter_by(**kwargs).first()

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


class WordService(ModelServiceBase):
    def __init__(self, session):
        ModelServiceBase.__init__(self, Word, session)
