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
	pass

@app.route('/catalog/new/')
def newCatalog():
	pass

@app.route('/catalog/<int:catalog_id>/edit/')
def editCatalog():
	pass

@app.route('/catalog/<int:catalog_id>/delete/')
def deleteCatalog():
	pass

@app.route('/catalog/<int:catalog_id>/category/')
def viewCategories():
	pass

@app.route('/catalog/<int:catalog_id>/category/new')
def newCategory():
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/edit/')
def editCategory():
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/delete/')
def deleteCategory():
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/')
def viewRecords():
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/newTemplate/')
def newRecordTemplate():
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/customTemplate/')
def newCustomTemplate():
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/new/')
def addRecord():
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/edit/')
def editRecord():
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/delete/')
def deleteRecord():
	pass

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/view/')
def showRecord():
	pass



























if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
