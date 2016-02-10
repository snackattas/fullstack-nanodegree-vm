import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship # to import foreign key relationships
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)

class Puppy(Base):
    __tablename__ = 'puppy'
    name = Column(String(250), nullable = False)
    date_of_birth = Column(Date)
    gender = Column("Sex", Enum(Sex))
    weight = Column(Integer)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = Relationship(Shelter)

class Sex(enum.Enum):
    male = "M"
    female = "F"

engine = create_engine('sqlite:///restaurantmenu.db') # can also use MySQL or postgres
Base.metadata.create_all(engine)
