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
def editCatalog(catalogID):
    return render_template('editCatalog.html')

@app.route('/catalog/<int:catalog_id>/delete/')
def deleteCatalog(catalogID):
    return render_template('deleteCatalog.html')

@app.route('/catalog/<int:catalog_id>/category/')
def viewCategories(catalogID):
    return render_template('viewCategories.html')

@app.route('/catalog/<int:catalog_id>/category/new')
def newCategory(catalogID):
    return render_template('newCategory.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/edit/')
def editCategory(catalogID):
    return render_template('editCategory.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/delete/')
def deleteCategory(catalogID):
    return render_template('deleteCategory.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/')
def viewRecords(catalogID, categoryID):
    return render_template('viewRecords.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/new/')
def newRecordTemplate(catalogID, categoryID):
    return render_template('recordTemplate.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/custom/')
def newCustomTemplate(catalogID, categoryID):
    return render_template('customTemplate.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/')
def addRecord(catalogID, categoryID):
    return render_template('addRecord.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/edit/')
def editRecord(catalogID, categoryID, recordID):
    return render_template('editRecord.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/delete/')
def deleteRecord(catalogID, categoryID, recordID):
    return render_template('deleteRecord.html')

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/view/')
def showRecord(catalogID, categoryID, recordID):
    return render_template('showRecord.html')



























if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
