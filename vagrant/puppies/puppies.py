from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import create_engine, select, func

Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('puppy_id', Integer, ForeignKey('puppy.id')),
                          Column('adopter.id', Integer, ForeignKey('adopter.id'))
                          )

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship("Shelter")
    weight = Column(Numeric(10))
    adopted = Column(Boolean, default=False)
    puppyprofile = relationship("PuppyProfile", uselist=False, back_populates='puppy')
    adopter = relationship('Adopter', secondary=association_table, back_populates='puppy')

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer)
    current_occupancy = column_property(
    select([func.count(Puppy.shelter_id)]).where(Puppy.shelter_id==id).correlate_except(Puppy))

class PuppyProfile(Base):
    __tablename__ = 'puppyprofile'
    id = Column(Integer, primary_key=True)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", back_populates='puppyprofile')
    photo = Column(String(300))
    description = Column(String(1000))
    special_needs = Column(String(250))

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", secondary=association_table, back_populates='adopter')
    first_name = Column(String(250))
    last_name = Column(String(250))


engine = create_engine('sqlite:///puppyshelter.db')


Base.metadata.create_all(engine)
