from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Catalog(Base):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    privacy = Column(Enum('public-readable',
                          'public-writeable',
                          'private'),
                           nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)

class RecordTemplate(Base):
    __tablename__ = 'record_template'

    id = Column(Integer, primary_key=True)
    custom = Column(Boolean, default=False)
    name = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    template_fields = relationship("FieldTemplate",
                                   back_populates="record_template")

class FieldTemplate(Base):
    __tablename__ = 'field_template'

    id = Column(Integer, primary_key=True)
    label = Column(String(250), nullable=False)
    kind = Column(Enum('short_text',
                        'long_text',
                        'drop_down',
                        'check_box',
                        'radio'),
                        nullable=False)
    record_template_id = Column(Integer, ForeignKey('record_template.id'))
    record_template = relationship("RecordTemplate",
                                    back_populates='template_fields')

class Option(Base):
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    field_template_id = Column(Integer, ForeignKey('field_template.id'))
    field_template = relationship(FieldTemplate)

class Record(Base):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    record_template_id = Column(Integer, ForeignKey('record_template.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    record_template = relationship(RecordTemplate)
    category = relationship(Category)


class Field(Base):
    __tablename__ = 'field'

    id = Column(Integer, primary_key=True)
    value = Column(String(500), nullable=False)
    record_id = Column(Integer, ForeignKey('record.id'))
    field_template_id = Column(Integer, ForeignKey('field_template.id'))
    record = relationship(Record)
    field_template = relationship(FieldTemplate)


engine = create_engine('sqlite:///catalogizer.db')

Base.metadata.create_all(engine)