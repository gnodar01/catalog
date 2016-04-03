from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import (Base, User, Catalog, Category, Record, Field,
							RecordTemplate, FieldTemplate, OptionTemplate)

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name='Goku', email='luv2battle@kamehouse.com')
session.add(User1)
session.commit()

catalog1 = Catalog(name='Battle-log', privacy='public', user_id=1)
session.add(catalog1)
session.commit()

category1 = Category(name='KI Blasts', catalog_id=1)
session.add(category1)
session.commit()

recordTemplate1 = RecordTemplate(category_id=1, name='Kamehameha Template')
session.add(recordTemplate1)
session.commit()

fieldTemplate1 = FieldTemplate(name='Blast Name', kind='short_text', record_template_id=1)
session.add(fieldTemplate1)
session.commit()

fieldTemplate2 = FieldTemplate(name='Damage (min-max)', kind='check_box', record_template_id=1)
session.add(fieldTemplate2)
session.commit()

optionTemplate1 = OptionTemplate(name='1', field_template_id=2)
session.add(optionTemplate1)
session.commit()

optionTemplate2 = OptionTemplate(name='2', field_template_id=2)
session.add(optionTemplate2)
session.commit()

optionTemplate3 = OptionTemplate(name='3', field_template_id=2)
session.add(optionTemplate3)
session.commit()

optionTemplate4 = OptionTemplate(name='4', field_template_id=2)
session.add(optionTemplate4)
session.commit()

optionTemplate5 = OptionTemplate(name='5', field_template_id=2)
session.add(optionTemplate5)
session.commit()

optionTemplate6 = OptionTemplate(name='Over 9000!!!', field_template_id=2)
session.add(optionTemplate6)
session.commit()

fieldTemplate3 = FieldTemplate(name='Charge Time', kind='drop_down', record_template_id=1)
session.add(fieldTemplate3)
session.commit()

optionTemplate6 = OptionTemplate(name='A couple seconds', field_template_id=3)
session.add(optionTemplate6)
session.commit()

optionTemplate7 = OptionTemplate(name='A couple minutes', field_template_id=3)
session.add(optionTemplate7)
session.commit()

optionTemplate8 = OptionTemplate(name='A couple episodes', field_template_id=3)
session.add(optionTemplate8)
session.commit()

optionTemplate9 = OptionTemplate(name='Depends on the mood', field_template_id=3)
session.add(optionTemplate9)
session.commit()

fieldTemplate4 = FieldTemplate(name='Blast Description', kind='long_text', record_template_id=1)
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

field5 = Field(value='Developed my the turtle sage himself.', record_id=1, field_template_id=4)
session.add(field5)
session.commit()


print "Database populated!"