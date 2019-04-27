from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Authors, Base, Novels, Users
import datetime

engine = create_engine('sqlite:///authorlibrarywithusersandtime.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()



# Menu for UrbanBurger
user = Users(name="abhi1111", picture="aapota1111", email = "hrabhijith@gmail.com")
session.add(user)
session.commit()

restaurant1 = Authors(name = "Benjamin Franklin", user = user )

session.add(restaurant1)
session.commit()

menuItem2 = Novels(name = "Egg cake story", description = "Soft baked egg cake", year = "1989", lastAdded = datetime.datetime.now(), author = restaurant1, user = user)

session.add(menuItem2)
session.commit()
