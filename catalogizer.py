from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine
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
    return render_template('showRecord.html', catalog=catalog, category=category, record=record)


# Helper functions to filter through and get database elements

def getCatalogs():
    catalogs = session.query(Catalog).all()
    return catalogs

def getCatalog(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    return catalog

def getCategories(catalog_id):
    categories = session.query(Category).filter_by(catalog_id=catalog_id).all()
    return categories

def getCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return category

def getRecord(record_id):
    record = session.query(Record).filter_by(id=record_id).one()
    return record

def getRecords(category_id):
    records = session.query(Record).filter_by(category_id=category_id).all()
    return records
























if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
