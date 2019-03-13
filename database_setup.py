import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Authors(Base):
    __tablename__ = 'authors'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class Novels(Base):
    __tablename__ = 'novels'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    year = Column(Integer)
    description = Column(String(250))
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship(Authors)

@property
def serialize(self):
   pass

engine = create_engine('sqlite:///authorlibrary.db')

Base.metadata.create_all(engine)