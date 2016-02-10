# if you want to import this into a python IDE and insert values:
# from sqlalchemy import create_engine
# from sqlalchem.orm import sessionmaker
# from database_setup import Base, Restaurant, MenuItem
# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind = engine)
# session = DBSession()
# myFirstRestaurant = Restaurant(name = "Pizza Palace")
# session.add(myFirstRestaurant)
# session.commit()
# session.query(Restaurant).all()
# cheesepizza = MenuItem(
# name = "Cheese Pizza",
# description = "Made with all natural ingredients and fresh mozzarella",
# course = "Entree",
# price = "$8.99",
# restaurant = myFirstRestaurant)
# session.add(cheesepizza)
# session.commit()
# session.query(MenuItem).all()


import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship # to import foreign key relationships
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant) # this line and the one above go together pretty  much
###At END OF DB ####
engine = create_engine('sqlite:///restaurantmenu.db') # can also use MySQL or postgres
Base.metadata.create_all(engine)
