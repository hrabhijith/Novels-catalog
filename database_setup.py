import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import create_engine

Base = declarative_base()

class Authors(Base):
    __tablename__ = 'authors'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
        return {
       'name' : self.name,
       'id' : self.id
        }

class Novels(Base):
    __tablename__ = 'novels'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    year = Column(Integer)
    description = Column(String(250))
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship(Authors, backref='novels')
    @property
    def serialize1(self):
        return {
       'name' : self.name,
       'id' : self.id,
       'author_id': self.author_id,
       'year': self.year,
       'description': self.description
        }






engine = create_engine('sqlite:///authorlibrary.db')

Base.metadata.create_all(engine)