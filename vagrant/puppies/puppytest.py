from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy, PuppyProfile, Adopter
import datetime
import string
import random
from random import randint

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
def puppies_alphabetical():
    for puppy in session.query(Puppy).order_by(Puppy.name.desc()):
        print str(puppy.id) + str(puppy.name) + " " + str(puppy.shelter_id) + " " + str(puppy.adopted)
def six_months():
    return datetime.date.today() - datetime.timedelta(days=183)
def puppy_age():
    six_months_ago = six_months()
    for puppy in session.query(Puppy).order_by(Puppy.dateOfBirth.desc()).filter(Puppy.dateOfBirth > six_months_ago):
        name = "Name: %s " % (puppy.name)
        print name.ljust(20) + "DOB: %s" % (puppy.dateOfBirth)
def puppy_weight():
    for puppy in session.query(Puppy).order_by(Puppy.weight):
        name = "Name: %s " % (puppy.name)
        print name.ljust(20) + "Weight: %s" % (puppy.weight)
def puppy_by_shelter():
    q = session.query(Puppy).join(Shelter).order_by(Shelter.name, Puppy.name)
    for puppy in q:
        name = "Name: %s" % (puppy.name)
        shelter = "Shelter: %s" % (puppy.shelter.name)
        print name.ljust(25) + shelter
def create_profiles():
    query = session.query(Puppy)
    for puppy in query:
        new_profile = PuppyProfile(puppy_id = puppy.id,
                       photo = 'http://media.mydogspace.com.s3.amazonaws.com/wp-content/uploads/2013/08/puppy-500x350.jpg',
                       description = 'a good critter!',
                       special_needs = 'love')
        session.add(new_profile)
        session.commit()
def look_profile():
    query = session.query(PuppyProfile).all()
    for puppy in query:
        print puppy.id," ", puppy.photo
def create_adopters():
    query = session.query(Puppy)
    for (i, puppy) in enumerate(query):
        if i < 50:
            new_adopter = Adopter(puppy_id = puppy.id,
                       first_name = 'Zach',
                       last_name = 'Attas')
            session.add(new_adopter)
        if i > 49:
            new_adopter = Adopter(puppy_id = 51,
                       first_name = 'Zach'+random.choice(string.letters),
                       last_name = 'Attas'+random.choice(string.letters))
            session.add(new_adopter)
        session.commit()
def look_adopter():
    query = session.query(Adopter).all()
    for adopter in query:
        print adopter.id," ",adopter.puppy_id," ",adopter.first_name," ", adopter.last_name
def look_shelter():
    query = session.query(Shelter).all()
    for shelter in query:
        print "Name: %s ID: %s Maximum capacity: %s current_occupancy: %s " % (shelter.name, shelter.id, shelter.maximum_capacity, shelter.current_occupancy)
def count_puppies_left(shelter_id):
    shelter_query = session.query(Shelter)
    the_shelter =  shelter_query.filter_by(id=shelter_id)
    puppies_left = the_shelter[0].maximum_capacity - the_shelter[0].current_occupancy
    return puppies_left

def check_in(name, gender, dateOfBirth, picture, weight, shelter_id):
        #Pass in ID
        #First establish room in the shelter
        shelter_query = session.query(Shelter)
        puppies_left = count_puppies_left(shelter_id)
        string = ''
        if puppies_left > 0:
            new_puppy = Puppy(name = name, gender = gender, dateOfBirth = dateOfBirth, picture = picture, shelter_id = shelter_id, weight = weight)
            session.add(new_puppy)
            session.commit()
        else:
            for shelters in shelter_query:
                puppies_left = count_puppies_left(shelters.id)
                if puppies_left > 0:
                    string += "ID: %s Name: %s" % (shelters.id, shelters.name) + "\n"
            if string:
                string = "That shelter is full.  Pick a new shelter: \n" + string + "\n" + "Your choice? "
                new_shelter = input(string)
                check_in(name, gender, dateOfBirth, picture, weight, new_shelter)
            else:
                return 'No more capacity for puppes :('
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday
def load_balancer():
    return ''

def adopt_puppy(puppy_id, adopters):
    """Adopter's name must be first and last, separated by a space
        If multiple adopters, they must be passed in as an array"""
    for adopter in adopters:
        first_name, last_name = adopter.split(' ')
        new_adopter = Adopter(puppy_id = puppy_id, first_name = first_name, last_name = last_name)
        session.add(new_adopter)
    if puppy_id:
        puppy_query = session.query(Puppy).filter_by(id=puppy_id).update({'shelter_id': '', 'adopted': True})
    session.commit()



#import puppytest
#(engine,DBSession,session) = puppytest.create()
