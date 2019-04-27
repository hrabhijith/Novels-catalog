# !/usr/bin/env python3
# !/usr/bin/python -3.5.2

from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import exc
from database_setup import Authors, Base, Novels, Users
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import jsonify
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import datetime
import sys

app = Flask(__name__)

# Fetching client ID for Google signin
CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']


# Creates sqlite DB connection and return session object
def dbConnection():
    try:
        engine = create_engine('sqlite:///authorlibrarywithusersandtime.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
    except exc.SQLAlchemyError as e:
        print(e)
        print("Unable to connect to the database")
        sys.exit(1)
    return session


# Authors list home page route
@app.route('/')
@app.route('/home/', methods=['GET'])
def categoryHomePage():
    # Checking whether user has logged in or not
    if 'username' not in login_session:
        login = 0
    else:
        login = 1

    # Creating DB connection and fetching authors list
    session = dbConnection()
    authors = session.query(Authors).all()

    # Fetching data to display recently added novels
    latestList = []
    novels = session.query(Novels).order_by(
        Novels.lastAdded.desc()).limit(10).all()
    if novels is not None:
        for i in novels:
            latestDict = {'author': '', 'novel': ''}
            latestDict['novel'] = i.name
            j = session.query(Authors).filter_by(id=i.author_id).one()
            latestDict['author'] = j.name
            latestList.append(latestDict)
    
    else:
        latestList = None

    session.close()

    return render_template('categorypage.html', authors=authors,
                           latest=latestList, login=login)


# Authors' novels page route
@app.route('/home/<int:author_id>/', methods=['GET'])
def categoryDetail(author_id):
    # Creating DB connection and fetching novels list for selected author
    session = dbConnection()
    author = session.query(Authors).filter_by(id=author_id).one()
    novels = session.query(Novels).filter_by(author_id=author_id).all()
    session.close()

    # Checking whether user has logged in or not
    if 'username' not in login_session:
        login = 0
    else:
        login = 1

    # Fetching id of the user if logged in else assigning 'None'
    try:
        creator_id = login_session['user_id']
    except KeyError:
        creator_id = None

    return render_template('categoryitemspage.html', novels=novels,
                           author=author, creator_id=creator_id, login=login)


# Edit novel details page route
@app.route('/home/<int:author_id>/<int:novel_id>/edit',
           methods=['GET', 'POST'])
def itemEdit(author_id, novel_id):
    # Token 1 for rendering novel details edit template
    token = 1

    # Creating DB connection
    session = dbConnection()

    # POST method functionality
    if request.method == 'POST':
        novel = session.query(Novels).filter_by(id=novel_id).one()

        if request.form['editedName']:
            novel.name = request.form['editedName']
            # Message to display when name is edited
            flash('A novel name was just edited')

        if request.form['editedYear']:
            novel.year = request.form['editedYear']
            # Message to display when year is edited
            flash('A novel year was just edited')

        # Adding and commiting changes to DB
        session.add(novel)
        session.commit()
        session.close()

        return redirect(url_for('categoryDetail', author_id=author_id))

    author = session.query(Authors).filter_by(id=author_id).one()
    novel = session.query(Novels).filter_by(id=novel_id).one()
    session.close()

    return render_template('edititempage.html',
                           token=token, novel=novel, author=author)


# Delete novel page route
@app.route('/home/<int:author_id>/<int:novel_id>/delete',
           methods=['GET', 'POST'])
def itemDelete(author_id, novel_id):

    # Creating DB connection
    session = dbConnection()

    # POST method functionality
    if request.method == 'POST':

        # Fetching the selected novel, deleting and commiting change
        novel = session.query(Novels).filter_by(id=novel_id).one()
        session.delete(novel)
        session.commit()
        session.close()
        # Message to display when a novel is deleted
        flash('A novel was just deleted')

        return redirect(url_for('categoryDetail', author_id=author_id))

    author = session.query(Authors).filter_by(id=author_id).one()
    novel = session.query(Novels).filter_by(id=novel_id).one()
    session.close()

    return render_template('deleteitempage.html', novel=novel, author=author)


# New novel page route
@app.route('/home/<int:author_id>/new', methods=['GET', 'POST'])
def itemNew(author_id):
    # Creating DB connection
    session = dbConnection()

    # Redirect to login page if user is not logged in
    if 'username' not in login_session:
        return redirect('/login')

    # POST method functionality
    if request.method == 'POST':

        # Selecting the author, creating new novel, addng and commiting changes
        author = session.query(Authors).filter_by(id=author_id).one()
        newNovel = Novels(name=request.form['newName'],
                          year=request.form['newYear'],
                          description=request.form['newDescription'],
                          lastAdded=datetime.datetime.now(),
                          author_id=author_id,
                          user_id=login_session['user_id'])
        session.add(newNovel)
        session.commit()
        session.close()
        # Message to display when a novel is added
        flash('A novel was just created')

        return redirect(url_for('categoryDetail', author_id=author_id))

    author = session.query(Authors).filter_by(id=author_id).one()
    session.close()

    return render_template('newitempage.html', author=author)


# Novel's description page route
@app.route('/home/<int:author_id>/<int:novel_id>/description/',
           methods=['GET'])
def categoryDescription(author_id, novel_id):
    # Creating DB connection
    session = dbConnection()

    # Fetching author and novel data to display description
    author = session.query(Authors).filter_by(id=author_id).one()
    novel = session.query(Novels).filter_by(id=novel_id).one()
    session.close()

    # Fetching id of the user if logged in else assigning 'None'
    try:
        creator_id = login_session['user_id']
    except KeyError:
        creator_id = None

    return render_template('descriptionpage.html',
                           novel=novel, author=author, creator_id=creator_id)


# Edit novel description page route
@app.route('/home/<int:author_id>/<int:novel_id>/description/edit',
           methods=['GET', 'POST'])
def descriptionEdit(author_id, novel_id):
    # Token 2 for rendering novel's description edit template
    token = 2

    # Creating DB connection
    session = dbConnection()

    # POST method functionality
    if request.method == 'POST':
        # Fetching novel data and adding edited
        # description and commiting changes
        novel = session.query(Novels).filter_by(id=novel_id).one()
        if request.form['editedDescription']:
            novel.description = request.form['editedDescription']
            session.add(novel)
            # Message to display when a novel description is edited
            flash('Novel description was just edited')

        session.commit()
        session.close()

        return redirect(url_for('categoryDescription',
                        author_id=author_id, novel_id=novel_id))

    author = session.query(Authors).filter_by(id=author_id).one()
    novel = session.query(Novels).filter_by(id=novel_id).one()
    session.close()

    return render_template('edititempage.html',
                           token=token, novel=novel, author=author)


# JSON endpoint API route
@app.route('/library.json')
def libraryJSON():
    # Creating DB connection
    session = dbConnection()

    # Fetching author and related novel details together
    authors = session.query(Authors).options(joinedload(Authors.novels)).all()

    # Returning JSONified author and novel data of entire DB
    return jsonify(Authors=[dict(c.serialize,
                   Novels=[i.serialize1 for i in c.novels])for c in authors])


# Login page route
@app.route('/login')
def showLogin():
    # Creating state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    # Storing state token in the login session
    login_session['state'] = state

    # Passing state taken to client side
    return render_template('login.html', STATE=state)


# Method to create user in DB using login session
def createUser(login_session):
    session = dbConnection()
    newUser = Users(name=login_session['username'],
                    picture=login_session['picture'],
                    email=login_session['email'])
    session.add(newUser)
    session.commit()
    session.close()
    user = session.query(Users).filter_by(email=login_session['email']).first()
    return user.id


# Method to get user object using user id
def getUserInfo(user_id):
    session = dbConnection()
    user = session.query(Users).filter_by(id=user_id).one()
    session.close()
    return user


# Method to get user id using email provided
def getUserId(email):
    session = dbConnection()
    try:
        user = session.query(Users).filter_by(email=email).first()
        session.close()
        return user.id
    except exc.SQLAlchemyError as e:
        print(e)
        return None


# Google signin route
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the user is already logged in or not
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # Storing the user data inside login session
    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # If user not present create user
    user = getUserId(login_session['email'])
    if user is None:
        id = createUser(login_session)
        login_session['user_id'] = id
    else:
        login_session['user_id'] = user

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
             -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    # Message to display when the user logs in
    flash("you are now logged in as %s" % login_session['username'])

    return output


# Logout functionality route
@app.route('/disconnect')
def disconnect():

    # Google logout functionality
    if login_session['provider'] == 'google':

        # Fetch access token from login session
        access_token = login_session.get('access_token')

        # Return error message if no access token
        if access_token is None:
            response = make_response(json.dumps(
                "Current user not connected."), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Sending logout request and getting status code
        url = 'https://accounts.google.com/o/oauth2/revoke'
        params = {'token': access_token, 'alt': 'json'}
        result = requests.get(url, params=params, headers={
                              'content-type':
                              'application/x-www-form-urlencoded'})
        status_code = getattr(result, 'status_code')

        # If status code is 200, deleting login session data
        if status_code == 200:
            del login_session['gplus_id']
            del login_session['username']
            del login_session['picture']
            del login_session['email']
            del login_session['user_id']
            del login_session['access_token']
            del login_session['state']
            # Message to display when the user logs out
            flash("Logged out Successfully!")
            # Redirecting to home page
            return redirect('/')

        # If status code is not 200
        else:
            response = make_response(json.dumps(
                'Failed to revoke connection.'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response

    # Facebook logout functionality
    if login_session['provider'] == 'facebook':
        # Fetching facebook id and access token from login session
        facebook_id = login_session['facebook_id']
        access_token = login_session['access_token']

        # If no access token, returning error message
        if access_token is None:
            response = make_response(json.dumps(
                "Current user not connected."), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Sending logout request
        url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
            facebook_id, access_token)
        h = httplib2.Http()
        result = h.request(url, 'DELETE')[1].decode('utf-8')
        res = json.loads(result)

        # If response contains success, deleting login session data
        if res['success'] is True:
            del login_session['username']
            del login_session['picture']
            del login_session['email']
            del login_session['user_id']
            del login_session['access_token']
            del login_session['state']
            # Message to display when user logs out
            flash("Logged out Successfully!")
            # Redirect to home page
            return redirect('/')

        # If response doesn't contains success
        else:
            response = make_response(json.dumps(
                'Failed to revoke connection.'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response


# Facebook signin route
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Fetching short-time access token from client,
    # app id and app secret from stored json file
    access_token = request.data.decode('utf-8')
    app_id = json.loads(open('fb_client_secret.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secret.json', 'r').read())['web']['app_secret']

    # Exchanging short-time token for login-time token
    url = '''https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=fb_exchange_token&fb_exchange_token=%s''' % (
            app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf-8')
    token = result.split(',')[0].split(':')[1].replace('"', '')

    # Checking if user already logged in or not, if not return error message
    stored_access_token = login_session.get('access_token')
    if stored_access_token is not None:
        response = make_response(json.dumps
                                 ('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Sending request to fetch user data
    url = '''https://graph.facebook.com/v3.2/me?access_token=%s&fields=name,id,email''' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf-8')

    # Storing user data in login session
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # If user not present create user
    user = getUserId(login_session['email'])
    if user is None:
        id = createUser(login_session)
        login_session['user_id'] = id
    else:
        login_session['user_id'] = user

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = '''https://graph.facebook.com/v3.2/me/picture?access_token=%s&redirect=0&height=200&width=200''' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf-8')
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
                -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    # Message to display when the user logs in
    flash("Now logged in as %s" % login_session['username'])

    return output


# Server host listening starts
if __name__ == '__main__':
    app.secret_key = 'super_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
