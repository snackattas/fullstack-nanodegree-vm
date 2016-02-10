from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def sheltertest():
    items = session.query(Shelter).all()
    for item in items:
        print str(item.id)+" "+item.name
#sheltertest()

def puppytest():
    items = session.query(Puppy).all()
    for item in items:
        print str(item.id)+" "+item.name
#puppytest()

def create():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from puppies import Base, Shelter, Puppy

    engine = create_engine('sqlite:///puppyshelter.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return (engine,DBSession,session)
