from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import (Base, User, Catalog, Category, Record, Field,
                            RecordTemplate, FieldTemplate, Option)

APPLICATION_NAME = "Catalogizer"

engine = create_engine('sqlite:///catalogizer.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog/')
def viewCatalogs():
    catalogs = getCatalogs()
    return render_template('viewCatalogs.html', catalogs=catalogs)

@app.route('/catalog/new/')
def newCatalog():
    return render_template('newCatalog.html')

@app.route('/catalog/<int:catalog_id>/edit/')
def editCatalog(catalog_id):
    catalog = getCatalog(catalog_id)
    return render_template('editCatalog.html', catalog=catalog)

@app.route('/catalog/<int:catalog_id>/delete/')
def deleteCatalog(catalog_id):
    catalog = getCatalog(catalog_id)
    return render_template('deleteCatalog.html', catalog=catalog)

@app.route('/catalog/<int:catalog_id>/category/')
def viewCategories(catalog_id):
    catalog = getCatalog(catalog_id)
    categories = getCategories(catalog_id)
    return render_template('viewCategories.html', catalog=catalog, categories=categories)

@app.route('/catalog/<int:catalog_id>/category/new')
def newCategory(catalog_id):
    catalog = getCatalog(catalog_id)
    return render_template('newCategory.html', catalog=catalog)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/edit/')
def editCategory(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    return render_template('editCategory.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/delete/')
def deleteCategory(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    return render_template('deleteCategory.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/')
def viewRecords(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    records = getRecords(category_id)
    return render_template('viewRecords.html', catalog=catalog, category=category, records=records)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/new/')
def newRecordTemplate(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    return render_template('recordTemplate.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/custom/')
def newCustomTemplate(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    return render_template('customTemplate.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/')
def addRecord(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    return render_template('addRecord.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/edit/')
def editRecord(catalog_id, category_id, record_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    record = getRecord(record_id)
    return render_template('editRecord.html', catalog=catalog, category=category, record=record)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/delete/')
def deleteRecord(catalog_id, category_id, record_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    record = getRecord(record_id)
    return render_template('deleteRecord.html', catalog=catalog, category=category, record=record)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/view/')
def showRecord(catalog_id, category_id, record_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    record = getRecord(record_id)
    fields = getFields(record_id)
    return render_template('showRecord.html', catalog=catalog, category=category, record=record, fields=fields)


# Helper functions to filter through and get database elements

def getCatalogs():
    return session.query(Catalog).all()

def getCatalog(catalog_id):
    return session.query(Catalog).filter_by(id=catalog_id).one()

def getCategories(catalog_id):
    return session.query(Category).filter_by(catalog_id=catalog_id).all()

def getCategory(category_id):
    return session.query(Category).filter_by(id=category_id).one()

def getRecord(record_id):
    return session.query(Record).filter_by(id=record_id).one()

def getRecords(category_id):
    return session.query(Record).filter_by(category_id=category_id).all()

def getFields(record_id):
    record = getRecord(record_id)
    fieldTemplates = session.query(FieldTemplate).filter_by(record_template_id=record.record_template_id).order_by(asc(FieldTemplate.id))
    fields = []

    for fieldTemplate in fieldTemplates:
        fieldLabel = fieldTemplate.label
        valueList = session.query(Field).filter_by(field_template_id=fieldTemplate.id).all()
        fieldValues = []
        for v in valueList:
            fieldValues.append(v.value)
        fields.append( (fieldLabel, fieldValues) )

    return fields

















if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
