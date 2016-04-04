from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import (Base, User, Catalog, Category, Record, Field,
							RecordTemplate, FieldTemplate, Option)

engine = create_engine('sqlite:///catalogizer.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name='Goku', email='luv2battle@kamehouse.com')
session.add(User1)
session.commit()

catalog1 = Catalog(name='Battle-log', privacy='public-readable', user_id=1)
session.add(catalog1)
session.commit()

category1 = Category(name='KI Blasts', catalog_id=1)
session.add(category1)
session.commit()

recordTemplate1 = RecordTemplate(category_id=1, name='Kamehameha Template')
session.add(recordTemplate1)
session.commit()

fieldTemplate1 = FieldTemplate(label='Blast Name', kind='short_text', record_template_id=1)
session.add(fieldTemplate1)
session.commit()

fieldTemplate2 = FieldTemplate(label='Damage (min-max)', kind='check_box', record_template_id=1)
session.add(fieldTemplate2)
session.commit()

option1 = Option(name='1', field_template_id=2)
session.add(option1)
session.commit()

option2 = Option(name='2', field_template_id=2)
session.add(option2)
session.commit()

option3 = Option(name='3', field_template_id=2)
session.add(option3)
session.commit()

option4 = Option(name='4', field_template_id=2)
session.add(option4)
session.commit()

option5 = Option(name='5', field_template_id=2)
session.add(option5)
session.commit()

option6 = Option(name='Over 9000!!!', field_template_id=2)
session.add(option6)
session.commit()

fieldTemplate3 = FieldTemplate(label='Charge Time', kind='drop_down', record_template_id=1)
session.add(fieldTemplate3)
session.commit()

option6 = Option(name='A couple seconds', field_template_id=3)
session.add(option6)
session.commit()

option7 = Option(name='A couple minutes', field_template_id=3)
session.add(option7)
session.commit()

option8 = Option(name='A couple episodes', field_template_id=3)
session.add(option8)
session.commit()

option9 = Option(name='Depends on the mood', field_template_id=3)
session.add(option9)
session.commit()

fieldTemplate4 = FieldTemplate(label='Blast Description', kind='long_text', record_template_id=1)
session.add(fieldTemplate4)
session.commit()

record1 = Record(name='Kamehameha Blast', record_template_id=1, category_id=1)
session.add(record1)
session.commit()

field1 = Field(value='Kamehameha', record_id=1, field_template_id=1)
session.add(field1)
session.commit()

field2 = Field(value='2', record_id=1, field_template_id=2)
session.add(field2)
session.commit()

field3 = Field(value='Over 9000!!!', record_id=1, field_template_id=2)
session.add(field3)
session.commit()

field4 = Field(value='Depends on the mood', record_id=1, field_template_id=3)
session.add(field4)
session.commit()

field5 = Field(value='Developed by the turtle sage himself.', record_id=1, field_template_id=4)
session.add(field5)
session.commit()


print "Database populated!"