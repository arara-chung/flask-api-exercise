from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()
class User(Base):

	# define tables
	__tablename__ = 'user'

	# define columns
	id = Column(Integer, primary_key=True)
	username = Column(String(32), index=True)
	password_hash = Column(String(64))

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	# define query response
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
       	   'id': self.id,
           'username': self.username,
        }

engine = create_engine('sqlite:///users.db')

Base.metadata.create_all(engine)
