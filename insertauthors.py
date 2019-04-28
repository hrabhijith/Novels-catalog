from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Authors, Base, Novels, Users
import datetime

engine = create_engine('sqlite:///authorlibrarywithusersandtime.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Menu for UrbanBurger
user = Users(name="abhi1111", picture="aapota1111",
             email="laharijma@gmail.com")
session.add(user)
session.commit()

restaurant1 = Authors(name="Stephen King", user=user)
session.add(restaurant1)
session.commit()

restaurant1 = Authors(name="J.R.R. Tolkien", user=user)
session.add(restaurant1)
session.commit()

restaurant1 = Authors(name="Charles Dickens", user=user)
session.add(restaurant1)
session.commit()

restaurant1 = Authors(name="J. K Rowling", user=user)
session.add(restaurant1)
session.commit()

restaurant1 = Authors(name="Fyodor Mikhailovich Dostoyevsky", user=user)
session.add(restaurant1)
session.commit()

restaurant1 = Authors(name="Edgar Allan Poe", user=user)
session.add(restaurant1)
session.commit()

restaurant1 = Authors(name="Mark Twain", user=user)
session.add(restaurant1)
session.commit()

restaurant1 = Authors(name="Dr. Seuss", user=user)
session.add(restaurant1)
session.commit()

restaurant1 = Authors(name="C.S. Lewis", user=user)
session.add(restaurant1)
session.commit()

restaurant1 = Authors(name="Roald Dah", user=user)
session.add(restaurant1)
session.commit()
