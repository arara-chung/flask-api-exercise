# -*- coding: utf-8 -*-

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

    # define query response
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