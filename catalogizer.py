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
	pass

@app.route('/catalog/<int:catalog_id>/edit/')
def editCatalog(catalogID):
	pass

@app.route('/catalog/<int:catalog_id>/delete/')
def deleteCatalog(catalogID):
	pass

@app.route('/catalog/<int:catalog_id>/category/')
def viewCategories(catalogID):
	pass

@app.route('/catalog/<int:catalog_id>/category/new')
def newCategory(catalogID):
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/edit/')
def editCategory(catalogID):
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/delete/')
def deleteCategory(catalogID):
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/')
def viewRecords(catalogID, categoryID):
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/new/')
def newRecordTemplate(catalogID, categoryID):
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/custom/')
def newCustomTemplate(catalogID, categoryID):
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/')
def addRecord(catalogID, categoryID):
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/edit/')
def editRecord(catalogID, categoryID, recordID):
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/delete/')
def deleteRecord(catalogID, categoryID, recordID):
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/view/')
def showRecord(catalogID, categoryID, recordID):
	pass



























if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
