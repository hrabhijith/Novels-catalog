import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(150))
    id = Column(Integer, primary_key=True)


class Authors(Base):
    __tablename__ = 'authors'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class Novels(Base):
    __tablename__ = 'novels'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    description = Column(String(250))
    lastAdded = Column(DateTime)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship(Authors, backref='novels')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize1(self):
        return {
            'name': self.name,
            'id': self.id,
            'author_id': self.author_id,
            'year': self.year,
            'description': self.description
        }


engine = create_engine('sqlite:///authorlibrarywithusersandtime.db')

Base.metadata.create_all(engine)
