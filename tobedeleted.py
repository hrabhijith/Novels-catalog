from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Authors, Base, Novels
 
engine = create_engine('sqlite:///authorlibrary.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()



#Menu for UrbanBurger
restaurant1 = Authors(name = "Second author")

session.add(restaurant1)
session.commit()

menuItem2 = Novels(name = "Egg cake story", description = "Soft baked egg cake", year = "1989", author = restaurant1)

session.add(menuItem2)
session.commit()
