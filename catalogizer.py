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
    catalogs = session.query(Catalog).all()
    return render_template('viewCatalogs.html', catalogs=catalogs)

@app.route('/catalog/new/')
def newCatalog():
    return render_template('newCatalog.html')

@app.route('/catalog/<int:catalog_id>/edit/')
def editCatalog(catalog_id):
    return render_template('editCatalog.html')

@app.route('/catalog/<int:catalog_id>/delete/')
def deleteCatalog(catalog_id):
    return render_template('deleteCatalog.html')

@app.route('/catalog/<int:catalog_id>/category/')
def viewCategories(catalog_id):
    return render_template('viewCategories.html')

@app.route('/catalog/<int:catalog_id>/category/new')
def newCategory(catalog_id):
    return render_template('newCategory.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/edit/')
def editCategory(catalog_id):
    return render_template('editCategory.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/delete/')
def deleteCategory(catalog_id):
    return render_template('deleteCategory.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/')
def viewRecords(catalog_id, category_id):
    return render_template('viewRecords.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/new/')
def newRecordTemplate(catalog_id, category_id):
    return render_template('recordTemplate.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/custom/')
def newCustomTemplate(catalog_id, category_id):
    return render_template('customTemplate.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/')
def addRecord(catalog_id, category_id):
    return render_template('addRecord.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/edit/')
def editRecord(catalog_id, category_id, record_id):
    return render_template('editRecord.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/delete/')
def deleteRecord(catalog_id, category_id, record_id):
    return render_template('deleteRecord.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/view/')
def showRecord(catalog_id, category_id, record_id):
    return render_template('showRecord.html')



























if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
