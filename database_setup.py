from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
	__tablename__ = 'user'


class Catalog(Base):
	__tablename__ = 'catalog'


class Category(Base):
	__tablename__ = 'category'


class Record(Base):
	__tablename__ = 'record'


class Field(Base):
	__tablename__ = 'field'


class Option(Base):
	__tablename__ = 'option'



engine = create_engine('sqlite:///catalogizer.db')

Base.metadata.create_all(engine)