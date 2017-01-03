# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

from flask import jsonify

Base = declarative_base()
class User(Base):

    # define tables
    __tablename__ = 'user'

    # define columns
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    # define query response: equivalent to getter setter
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'username': self.username
        }

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)



engine = create_engine('sqlite:///users.db')

Base.metadata.create_all(engine)


# ----------------------
# User methods: get, make, put, delete 
# ----------------------
def get_all_users(session):
    users = session.query(User).all()
    for user in users:
        print(users)
    return jsonify(users=[user.serialize for user in users])

