import random, string, httplib2, json, requests

from flask import Flask, render_template, request, redirect, url_for, flash, make_response
app = Flask(__name__)
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import (Base, User, Catalog, Category, Record, Field, RecordTemplate, FieldTemplate, Option)

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


APPLICATION_NAME = "Catalogizer"

# client id for google openID
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalogizer.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login/')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['Post'])
def gconnect():
    if request.args.get('state') != login_session.get('state'):
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object that can be used to authorize requests.
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = '')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the acces token is used for the intendend user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in.
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists and get Id assigned in database.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    updateUser(login_session['user_id'], 
               login_session['picture'], 
               login_session['username'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (' " style = "width: 300px; height: 300px;'
               'border-radius: 150px;-webkit-border-radius: 150px'
               ';-moz-border-radius: 150px;"> ')

    flash("Now logged in as %s" % login_session['username'])
    print login_session
    return output    

# DISCONNECT - Revoke a current user's token and reset their login_session.
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/')
@app.route('/catalog/')
def viewCatalogs():
    catalogs = getCatalogs()
    return render_template('viewCatalogs.html', catalogs=catalogs, current_user=login_session.get('user_id'))

@app.route('/catalog/new/', methods=['GET','POST'])
def newCatalog():
    if 'user_id' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        catalogName = request.form['catalog-name']
        newCatalogEntry = Catalog(name=catalogName, privacy='public-readable', user_id=login_session.get('user_id'))
        session.add(newCatalogEntry)
        session.commit()
        flash('%s successfully created!' % catalogName)
        return redirect(url_for('viewCatalogs'))
    else:
        return render_template('newCatalog.html')

@app.route('/catalog/<int:catalog_id>/edit/', methods=['GET','POST'])
def editCatalog(catalog_id):
    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can edit this catalog.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    if request.method == 'POST':
        newCatalogName = request.form['new-catalog-name']
        catalog.name = newCatalogName
        session.commit()
        flash('%s successfully edited!' % newCatalogName)
        return redirect(url_for('viewCatalogs'))
    else:
        return render_template('editCatalog.html', catalog=catalog)

@app.route('/catalog/<int:catalog_id>/delete/', methods=['GET','POST'])
def deleteCatalog(catalog_id):
    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can delete this catalog.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    if request.method == 'POST':
        delCatalog(catalog_id)
        return redirect(url_for('viewCatalogs'))
    else:
        return render_template('deleteCatalog.html', catalog=catalog)

@app.route('/catalog/<int:catalog_id>/category/')
def viewCategories(catalog_id):
    catalog = getCatalog(catalog_id)
    categories = getCategories(catalog_id)
    return render_template('viewCategories.html', catalog=catalog, categories=categories, current_user=login_session.get('user_id'))

@app.route('/catalog/<int:catalog_id>/category/new', methods=['GET','POST'])
def newCategory(catalog_id):
    if 'user_id' not in login_session:
        return redirect('/login')

    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can add a category to it.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    if request.method == 'POST':
        categoryName = request.form['category-name']
        categoryEntry = Category(name=categoryName, catalog_id=catalog.id)
        session.add(categoryEntry)
        session.commit()
        flash('%s successfully created!' % categoryName)
        return redirect(url_for('viewCategories', catalog_id=catalog.id))
    else:
        return render_template('newCategory.html', catalog=catalog)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/edit/', methods=['GET','POST'])
def editCategory(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can edit this category.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    category = getCategory(category_id)
    if request.method == 'POST':
        newCategoryName = request.form['new-category-name']
        category.name = newCategoryName
        session.commit()
        flash('%s successfully edited!' % newCategoryName)
        return redirect(url_for('viewCategories', catalog_id=catalog_id))
    else:
        return render_template('editCategory.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/delete/', methods=['GET','POST'])
def deleteCategory(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can delete this category.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    if request.method == 'POST':
        delCategory(category_id)
        return redirect(url_for('viewCategories', catalog_id=catalog_id))
    else:
        category = getCategory(category_id)
        return render_template('deleteCategory.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/')
def viewRecords(catalog_id, category_id):
    catalog = getCatalog(catalog_id)
    category = getCategory(category_id)
    records = getRecordsByCategoryId(category_id)
    return render_template('viewRecords.html', catalog=catalog, category=category, records=records, current_user=login_session.get('user_id'))

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/')
def addRecord(catalog_id, category_id):
    if 'user_id' not in login_session:
        return redirect('/login')

    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can add a new record to it.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    category = getCategory(category_id)
    recordTemplates = getRecordTemplates(category_id)
    return render_template('addRecord.html', catalog=catalog, category=category, rTemplates=recordTemplates, current_user=login_session.get('user_id'))

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/<int:record_template_id>/new/', methods=['GET','POST'])
def newRecord(catalog_id, category_id, record_template_id):
    if 'user_id' not in login_session:
        return redirect('/login')

    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can add a new record to it.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    if request.method == 'POST':
        recordName = request.form['record-name']
        addNewRecord(category_id, record_template_id)
        flash('%s successfully created!' % recordName)
        return redirect(url_for('viewRecords', catalog_id=catalog_id, category_id=category_id))
    else:
        category = getCategory(category_id)
        recordTemplate = getRecordTemplate(record_template_id)
        fieldTemplatesWithOptions = getFormattedFieldTemplatesWithOptions(record_template_id)
        return render_template('newRecord.html', catalog=catalog, category=category, rTemplate=recordTemplate, fTemplates=fieldTemplatesWithOptions)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/edit/', methods=['GET', 'POST'])
def editRecord(catalog_id, category_id, record_id):
    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can edit this record.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    record = getRecord(record_id)
    if request.method == 'POST':
        newName = request.form['record-name']
        record_template_id = record.record_template_id
        delRecord(record_id)
        addNewRecord(category_id, record_template_id)
        flash('%s successfully edited!' % newName)
        return redirect(url_for('viewRecords', catalog_id=catalog_id, category_id=category_id))
    else:
        category = getCategory(category_id)
        fieldTemplatesWithValues = getFieldTemplatesWithValues(record_id)
        return render_template('editRecord.html', catalog=catalog, category=category, record=record, fTemplates=fieldTemplatesWithValues)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/<int:record_id>/delete/', methods=['GET', 'POST'])
def deleteRecord(catalog_id, category_id, record_id):
    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can delete this record.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    if request.method == 'POST':
        record = getRecord(record_id)
        flash('%s successfully deleted!' % record.name)
        delRecord(record_id)
        return redirect(url_for('viewRecords', catalog_id=catalog_id, category_id=category_id))
    else:
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
    if 'user_id' not in login_session:
        return redirect('/login')

    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can add a record template for it.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

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

        flash('%s successfully created!' % recordTemplateName)
        return redirect(url_for('addRecord', catalog_id=catalog_id, category_id=category_id))
    else:
        category = getCategory(category_id)
        return render_template('recordTemplate.html', catalog=catalog, category=category)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/template/<int:record_template_id>/edit/', methods=['GET', 'POST'])
def editRecordTemplate(catalog_id, category_id, record_template_id):
    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can edit this record template.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    rTemplate = getRecordTemplate(record_template_id)
    if request.method == 'POST':
        newRecordTemplateName = request.form['new-rt-name']
        rTemplate.name = newRecordTemplateName
        session.commit()
        flash('%s successfully edited!' % newRecordTemplateName)
        return redirect(url_for('addRecord', catalog_id=catalog_id, category_id=category_id))
    else:
        catalog = getCatalog(catalog_id)
        category = getCategory(category_id)
        return render_template('editRecordTemplate.html', catalog=catalog, category=category, rTemplate=rTemplate)

@app.route('/catalog/<int:catalog_id>/category/<int:category_id>/record/add/template/<int:record_template_id>/delete/', methods=['GET', 'POST'])
def deleteRecordTemplate(catalog_id, category_id, record_template_id):
    catalog = getCatalog(catalog_id)
    if catalog.user_id != login_session.get('user_id'):
        flash('Only the owner of %s can delete this record template.' % catalog.name)
        return redirect(url_for('viewCatalogs'))

    if request.method == 'POST':
        delRecord_Template(record_template_id)
        return redirect(url_for('addRecord', catalog_id=catalog_id, category_id=category_id))
    else:
        category = getCategory(category_id)
        rTemplate = getRecordTemplate(record_template_id)
        return render_template('deleteRecordTemplate.html', catalog=catalog, category=category, rTemplate=rTemplate)


# Helper functions for adding new entries or updating entries

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    # user = session.query(User).filter_by(email=login_session['email']).one()
    # return user.id
    return newUser.id

def updateUser(user_id, picture, name):
    user = session.query(User).filter_by(id=user_id).one()
    change = False
    if user.picture != picture:
        user.picture = picture
        change = True
    if user.name != name:
        user.name = name
        change = True
    if change == True:
        session.commit()

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

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

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
            fieldTemplateDict['options'].append( (option.name, option.id) )

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

    flash('%s successfully deleted!' % recordTemplate.name)

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

    flash('%s successfully deleted!' % category.name)

    for recordTemplate in recordTemplates:
        delRecord_Template(recordTemplate.id)

    session.delete(category)
    session.commit()

def delCatalog(catalog_id):
    catalog = getCatalog(catalog_id)
    categories = getCategories(catalog_id)

    flash('%s successfully deleted!' % catalog.name)

    for category in categories:
        delCategory(category.id)

    session.delete(catalog)
    session.commit()




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
