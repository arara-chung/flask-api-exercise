# -*- coding: utf-8 -*-
from flask import jsonify

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Puppy(Base):

    # define tables
    __tablename__ = 'puppy'

    # define columns
    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))

    # define query response -- @property means getter setter
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
       	   'id': self.id,
           'name': self.name,
           'description' : self.description
        }

engine = create_engine('sqlite:///puppies.db', encoding='utf8')
Base.metadata.create_all(engine)



# ----------------------
# Puppy methods: get, make, put, delete 
# ----------------------

def getAllPuppies(session):
    puppies = session.query(Puppy).all()
    return jsonify(puppies=[i.serialize for i in puppies])
  
def makeANewPuppy(name, description, session):
    puppy = Puppy(name=name, description=description)
    session.add(puppy)
    session.commit()
    return jsonify(puppy=puppy.serialize) 

def getPuppy(id, session):
    puppy = session.query(Puppy).filter_by(id=id).one()
    return jsonify(puppy=puppy.serialize)
  
def updatePuppy(id, name, description, session):
    puppy = session.query(Puppy).filter_by(id=id).one()

    if name:
        puppy.name = name
    if description:
        puppy.description = description

    session.add(puppy)
    session.commit()

    return jsonify(message="Updating a Puppy with id %s" % id) 

def deletePuppy(id, session):
    puppy = session.query(Puppy).filter_by(id=id).one()

    session.delete(puppy)
    session.commit()

    return jsonify(message="Removing Puppy with id %s" % id)

