from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine #this binds our class definitions with their corresponding tables in our database
DBSession = sessionmaker(bind = engine)

session = DBSession()

myFirstRestaurant = Restaurant(name = 'Pizza Palace')
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()

cheesepizza = MenuItem(name = 'Cheese Pizza', description = 'dope',
                       course = 'Entree', price = '$8.99',
                       restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
session.query(Restaurant).all()

#with running lotsofmenus script
def itemtest():
    items = session.query(MenuItem).all()
    for item in items:
        print item.name
def Rest():
    firstResult = session.query(Restaurant).first()
    print firstResult.name
#updating a menu item
def Update():
    veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
    for veggieBurger in veggieBurgers:
        print veggieBurger.id
        print veggieBurger.price
        print veggieBurger.restaurant.name
        print "\n"
    UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 1).one()
    print 'Veggie Burg Price: ' + UrbanVeggieBurger.price

    for veggieBurger in veggieBurgers:
        if veggieBurger.price > '$7.50':
            veggieBurger.price = '$7.50'
            session.add(veggieBurger)
            session.commit()
    veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
    for veggieBurger in veggieBurgers:
        print veggieBurger.id
        print veggieBurger.price
        print veggieBurger.restaurant.name
        print "\n"
def Delete():
    spinach = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
    print spinach.restaurant.name
    session.delete(spinach)
    session.commit()
    spinach = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
