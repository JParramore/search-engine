from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Page(Base):
    __tablename__ = 'page'
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), default=func.now(), onupdate=func.now())
    id = Column(Integer, primary_key=True)
    url = Column(String())
    title = Column(String())
    description = Column(String())
    words = relationship('Word', secondary='location', backref='pages')


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    stem = Column(String(), index=True, unique=True)


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    word_id = Column(Integer, ForeignKey('word.id'))
    page_id = Column(Integer, ForeignKey('page.id'))
    page = relationship('Page', backref=backref('location'))
    word = relationship('Word', backref=backref('location'))