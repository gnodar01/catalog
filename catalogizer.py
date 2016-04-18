from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
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

@app.route('/catalog/new/', methods=['GET','POST'])
def newCatalog():
    if request.method == 'POST':
        catalogName = request.form['catalog-name']
        newCatalogEntry = Catalog(name=catalogName, privacy='public-readable', user_id=1)
        session.add(newCatalogEntry)
        session.commit()
        flash('%s successfully created!' % catalogName)
        return redirect(url_for('viewCatalogs'))
    else:
        return render_template('newCatalog.html')

@app.route('/catalog/<int:catalog_id>/edit/', methods=['GET','POST'])
def editCatalog(catalog_id):
    catalog = getCatalog(catalog_id)
    if request.method == 'POST':
        newCatalogName = request.form['new-catalog-name']
        catalog.name = newCatalogName
        session.commit()
        return redirect(url_for('viewCatalogs'))
    else:
        return render_template('editCatalog.html', catalog=catalog)

@app.route('/catalog/<int:catalog_id>/delete/', methods=['GET','POST'])
def deleteCatalog(catalog_id):
    catalog = getCatalog(catalog_id)
    if request.method == 'POST':
        delCatalog(catalog_id)
        return redirect(url_for('viewCatalogs'))
    else:
        return render_template('deleteCatalog.html', catalog=catalog)

@app.route('/catalog/<int:catalog_id>/category/')
def viewCategories(catalog_id):
    catalog = getCatalog(catalog_id)
    categories = getCategories(catalog_id)
    return render_template('viewCategories.html', catalog=catalog, categories=categories)

@app.route('/catalog/<int:catalog_id>/category/new', methods=['GET','POST'])
def newCategory(catalog_id):
    catalog = getCatalog(catalog_id)
    if request.method == 'POST':
        categoryName = request.form['category-name']
        categoryEntry = Category(name=categoryName, catalog_id=catalog.id)
        session.add(categoryEntry)
        session.commit()
        return redirect(url_for('viewCategories', catalog_id=catalog.id))
    else:
        return render_template('newCategory.html', catalog=catalog)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/edit/', methods=['GET','POST'])
def editCategory(catalog_id, category_id):
    category = getCategory(category_id)
    if request.method == 'POST':
        newCategoryName = request.form['new-category-name']
        category.name = newCategoryName
        session.commit()
        return redirect(url_for('viewCategories', catalog_id=catalog_id))
    else:
        catalog = getCatalog(catalog_id)
        return render_template('editCategory.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/delete/', methods=['GET','POST'])
def deleteCategory(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    if request.method == 'POST':
        delCategory(category_id)
        return redirect(url_for('viewCategories', catalog_id=catalog_id))
    else:
        catalog = getCatalog(catalog_id)
        category = getCategory(category_id)
        return render_template('deleteCategory.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/')
def viewRecords(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    records = getRecordsByCategoryId(category_id)
    return render_template('viewRecords.html', catalog=catalog, category=category, records=records)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/')
def addRecord(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    recordTemplates = getRecordTemplates(category_id)
    return render_template('addRecord.html', catalog=catalog, category=category, rTemplates=recordTemplates)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/<int:record_template_id>/new/', methods=['GET','POST'])
def newRecord(catalog_id, category_id, record_template_id):
    if request.method == 'POST':
        addNewRecord(category_id, record_template_id)
        return redirect(url_for('viewRecords', catalog_id=catalog_id, category_id=category_id))
    else:
        catalog = getCatalog(catalog_id)
        category = getCategory(category_id)
        recordTemplate = getRecordTemplate(record_template_id)
        fieldTemplatesWithOptions = getFormattedFieldTemplatesWithOptions(record_template_id)
        return render_template('newRecord.html', catalog=catalog, category=category, rTemplate=recordTemplate, fTemplates=fieldTemplatesWithOptions)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/edit/', methods=['GET', 'POST'])
def editRecord(catalog_id, category_id, record_id):
    record = getRecord(record_id)
    if request.method == 'POST':
        record_template_id = record.record_template_id
        delRecord(record_id)
        addNewRecord(category_id, record_template_id)
        return redirect(url_for('viewRecords', catalog_id=catalog_id, category_id=category_id))
    else:
        catalog = getCatalog(catalog_id)
        category = getCategory(category_id)
        fieldTemplatesWithValues = getFieldTemplatesWithValues(record_id)
        return render_template('editRecord.html', catalog=catalog, category=category, record=record, fTemplates=fieldTemplatesWithValues)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/delete/', methods=['GET', 'POST'])
def deleteRecord(catalog_id, category_id, record_id):
    if request.method == 'POST':
        delRecord(record_id)
        return redirect(url_for('viewRecords', catalog_id=catalog_id, category_id=category_id))
    else:
        catalog = getCatalog(catalog_id)
        category = getCategory(category_id)
        record = getRecord(record_id)
        return render_template('deleteRecord.html', catalog=catalog, category=category, record=record)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/view/')
def showRecord(catalog_id, category_id, record_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    record = getRecord(record_id)
    fields = getFormattedFields(record_id)
    return render_template('showRecord.html', catalog=catalog, category=category, record=record, fields=fields)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/template/', methods=['GET','POST'])
def newRecordTemplate(catalog_id, category_id):
    if request.method == 'POST':
        formData = request.form.copy()

        recordTemplateName = formData.pop('template-name')
        recordTemplateEntry = RecordTemplate(name=recordTemplateName, category_id=category_id)
        session.add(recordTemplateEntry)
        session.commit()

        for keyValue in formData.lists():
            groupIdentifier = keyValue[0][0:keyValue[0].find("-")]
            inputType = keyValue[0][keyValue[0].find("-") + 1:]
            if inputType == "field-kind":
                fieldTemplateLabel = formData.get(groupIdentifier + "-field-label")
                fieldTemplateKind = formData.get(groupIdentifier + "-field-kind")
                fieldTemplateOptions = formData.getlist(groupIdentifier + "-option")

                fieldTemplateEntry = FieldTemplate(label=fieldTemplateLabel, kind=fieldTemplateKind, order=groupIdentifier, record_template_id=recordTemplateEntry.id)
                session.add(fieldTemplateEntry)
                session.commit()

                while len(fieldTemplateOptions) > 0:
                    optionEntry = Option(name=fieldTemplateOptions.pop(0), field_template_id=fieldTemplateEntry.id)
                    session.add(optionEntry)
                    session.commit()

        return redirect(url_for('addRecord', catalog_id=catalog_id, category_id=category_id))
    else:
        catalog = getCatalog(catalog_id)
        category = getCategory(category_id)
        return render_template('recordTemplate.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/template/<int:record_template_id>/edit/', methods=['GET', 'POST'])
def editRecordTemplate(catalog_id, category_id, record_template_id):
    rTemplate = getRecordTemplate(record_template_id)
    if request.method == 'POST':
        newRecordTemplateName = request.form['new-rt-name']
        rTemplate.name = newRecordTemplateName
        session.commit()
        return redirect(url_for('addRecord', catalog_id=catalog_id, category_id=category_id))
    else:
        catalog = getCatalog(catalog_id)
        category = getCategory(category_id)
        return render_template('editRecordTemplate.html', catalog=catalog, category=category, rTemplate=rTemplate)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/template/<int:record_template_id>/delete/', methods=['GET', 'POST'])
def deleteRecordTemplate(catalog_id, category_id, record_template_id):
    if request.method == 'POST':
        delRecord_Template(record_template_id)
        return redirect(url_for('addRecord', catalog_id=catalog_id, category_id=category_id))
    else:
        catalog = getCatalog(catalog_id)
        category = getCategory(category_id)
        rTemplate = getRecordTemplate(record_template_id)
        return render_template('deleteRecordTemplate.html', catalog=catalog, category=category, rTemplate=rTemplate)

# Helper functions for adding new entries

def addNewRecord(category_id, record_template_id):
    # The request object is a Werkzeug data structure called ImmutableMultiDict, which has a copy method that returns a mutable Wekzeug MultiDict.
    formData = request.form.copy()
    # Pop the first item (the record name) for a list on the dict, and remove the key from the dict.
    recordName = formData.pop('record-name')
    newRecordEntry = Record(name=recordName, record_template_id=record_template_id, category_id=category_id)
    session.add(newRecordEntry)
    session.commit()

    # Call lists method on the formData multiDict, to get a list of tupples of keys and a list of all values corresponding to each unique key.
    for keyValues in formData.lists():
        fieldTemplateId = int(keyValues[0])
        fieldValues = keyValues[1]
        for fieldValue in fieldValues:
            # After calling session.commit() on the newRecordEntry, SQLAlchemy automatically reloads the object from the database, allowing access to its assigned primary key.
            newFieldEntry = Field(value=fieldValue, field_template_id=fieldTemplateId, record_id=newRecordEntry.id)
            session.add(newFieldEntry)
    session.commit()

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

def getRecordsByCategoryId(category_id):
    return session.query(Record).filter_by(category_id=category_id).all()

def getRecordsByRecordTemplateId(record_template_id):
    return session.query(Record).filter_by(record_template_id=record_template_id).all()

def getFields(record_id):
    return session.query(Field).filter_by(record_id=record_id).all()

def getRecordTemplate(record_template_id):
    return session.query(RecordTemplate).filter_by(id=record_template_id).one()

def getRecordTemplates(category_id):
    return session.query(RecordTemplate).filter_by(category_id=category_id).all()

def getFieldTemplates(record_template_id):
    return session.query(FieldTemplate).filter_by(record_template_id=record_template_id).order_by(asc(FieldTemplate.order))

def getOptions(field_template_id):
    return session.query(Option).filter_by(field_template_id=field_template_id).order_by(asc(Option.id))

def getFormattedFields(record_id):
    """Returns field labels and values in the form of an array of tupples of the field label and an array of the field values. E.g. [ ( field label, [field value1, field value2] ) ]"""
    record = getRecord(record_id)
    fieldTemplates = getFieldTemplates(record.record_template_id)
    fields = []

    for fieldTemplate in fieldTemplates:
        fieldLabel = fieldTemplate.label
        valueList = session.query(Field).filter_by(field_template_id=fieldTemplate.id, record_id=record.id).order_by(asc(Field.id))
        fieldValues = []
        for v in valueList:
            fieldValues.append(v.value)
        fields.append( (fieldLabel, fieldValues) )

    return fields

def getFormattedFieldTemplatesWithOptions(record_template_id):
    """Returns a list of dictionaries containing field template id, label, kind, and a list of options for that field template."""
    fieldTemplates = getFieldTemplates(record_template_id)
    fieldsWithOptions = []

    for fieldTemplate in fieldTemplates:
        fieldTemplateDict = {
            'id': fieldTemplate.id,
            'label': fieldTemplate.label,
            'kind': fieldTemplate.kind,
            'options': []
        }

        options = getOptions(fieldTemplate.id)
        for option in options:
            fieldTemplateDict['options'].append(option.name)

        fieldsWithOptions.append(fieldTemplateDict)

    return fieldsWithOptions

def getFieldTemplatesWithValues(record_id):
    record = getRecord(record_id)
    ftDictList = getFormattedFieldTemplatesWithOptions(record.record_template_id)

    for ftDict in ftDictList:
        ftDict['values'] = []
        ftId = ftDict['id']
        fields = session.query(Field).filter_by(field_template_id=ftId).all()
        for field in fields:
            value = field.value
            ftDict['values'].append(value)

    return ftDictList


# Helper functions to delete database items

def delRecord(record_id):
    record = getRecord(record_id)
    fields = getFields(record_id)
    for field in fields:
        session.delete(field)
        session.commit()
    session.delete(record)
    session.commit()


def delRecord_Template(record_template_id):
    recordTemplate = getRecordTemplate(record_template_id)
    fieldTemplates = getFieldTemplates(record_template_id)
    records = getRecordsByRecordTemplateId(record_template_id)

    for fieldTemplate in fieldTemplates:
        options = getOptions(fieldTemplate.id)
        for option in options:
            session.delete(option)
            session.commit()
        session.delete(fieldTemplate)
        session.commit()

    for record in records:
        delRecord(record.id)

    session.delete(recordTemplate)
    session.commit()

def delCategory(category_id):
    category = getCategory(category_id)
    recordTemplates = getRecordTemplates(category_id)

    for recordTemplate in recordTemplates:
        delRecord_Template(recordTemplate.id)

    session.delete(category)
    session.commit()

def delCatalog(catalog_id):
    catalog = getCatalog(catalog_id)
    categories = getCategories(catalog_id)

    for category in categories:
        delCategory(category.id)

    session.delete(catalog)
    session.commit()





if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
