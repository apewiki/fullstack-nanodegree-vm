from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc
from database import Base, Category, Item, User

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

CLIENT_ID = json.loads(
	open('client_secrets.json','r').read())['web']['client_id']
APPLICATION_NAME = 'spotscatalog'

def getCategory(category_id):
	return session.query(Category).filter_by(id = category_id).first()

def getAllCategories():
	return session.query(Category).all()

def createUser(login_session):
	newUser = User(name = login_session['username'], 
				picture = login_session.get('picture'),
				email = login_session['email'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email = login_session['email']).first()
	print "user is being created!"
	print user
	return user.id

def getUserID(login_session):
	print "************getting user id"

	user = session.query(User).filter_by(email = login_session['email']).first()
	print "*****got id"
	print user
	if user:
		return user.id
	else:
		return None

@app.route('/example')
def exmaple():
	return render_template('example.html')

@app.route('/')
@app.route('/catalog/')
def showCatalog():
	allow_edit = False
	if 'user_id' in login_session:
		allow_edit = True
	categories = session.query(Category).all()
	recentItems = session.query(Category.name, Item).filter(Category.id 
								== Item.category_id).order_by(Item.date_added.desc()).limit(5)
	print recentItems
	#flash('Testing flash!')
	return render_template('catalog.html', categories = categories, 
							recentItems = recentItems, allow_edit = allow_edit)


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/item')
def showItems(category_id):
	allow_edit = False
	print login_session
	if 'username' in login_session:
		print login_session['username']
		print login_session['user_id']
		allow_edit = True
	category = getCategory(category_id = category_id)
	categories = getAllCategories()
	items = session.query(Item).filter_by(category_id = category_id).all()
	return render_template('category.html', category  = category, 
							categories = categories,
							num_items = len(items), items= items, allow_edit = allow_edit)

@app.route('/catalog/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
	allow_edit = False
	c = session.query(Category).filter_by(id = category_id).first()
	i = session.query(Item).filter_by(category_id = category_id, id = item_id).first()
	showPic = False
	if i.picture and len(i.picture) > 0 and i.picture.endswith('jpg'):
		showPic = True
	if 'user_id' in login_session:
		allow_edit = (login_session['user_id'] == i.user_id)
	return render_template('item.html', category = c, item = i, 
							allow_edit = allow_edit, showPic = showPic)

@app.route('/catalog/<int:category_id>/new', methods = ['GET', 'POST'])
def addItem(category_id):
	if 'user_id' not in login_session:
		flash('Please login to add item.')
		return redirect(url_for('/login'))
	if request.method == 'POST':
		selectedCategory = str(request.form['selectedCategory'])
		print selectedCategory

		new_category_id = session.query(Category).filter_by(name = selectedCategory).first().id
		if new_category_id:
			category_id = new_category_id
			print category_id

		newItem = Item(name = request.form['itemName'], 
						description = request.form['itemDescription'],
						category_id = category_id,
						picture = request.form['imageFile'],
						price = request.form['itemPrice'],
						user_id = login_session['user_id'])
		session.add(newItem)
		session.commit()
		flash('New item is added!')
		return redirect(url_for('showItems', category_id = category_id))
	else:
		categories = getAllCategories()
		category = getCategory(category_id)
		return render_template('newItem.html', categories = categories, category = category)

@app.route('/catalog/<int:category_id>/item/<int:item_id>/edit', methods = ['GET', 'POST'])
def editItem(category_id, item_id):
	item = session.query(Item).filter_by(category_id = category_id, id = item_id).first()
	categories = getAllCategories()
	if request.method == 'POST':
		item.name = request.form['itemName']
		item.description = request.form['itemDescription']
		item.picture = request.form['itemImageFile']
		item.price = request.form['itemPrice']
		new_category_id = session.query(Category).filter_by(name = request.form['itemCategory']).first().id
		if new_category_id:
			category_id = new_category_id
			item.category_id = new_category_id
		if item.name and new_category_id:
			session.commit()
			flash('Item %s has been modified!' % item.name)
			return redirect(url_for('showItems', category_id = category_id))
		else:
			flash('Please input title of the item and select category.')
			return render_template('editItem.html', categories = categories, 
								category_id = category_id, item = item)
	else:
		return render_template('editItem.html', categories = categories, 
								category_id = category_id, item = item)

@app.route('/catalog/<int:category_id>/item/<int:item_id>/delete', methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
	item = session.query(Item).filter_by(category_id = category_id, id = item_id).first()
	name = item.name
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash("Item %s has been deleted!" % name)
		return redirect(url_for('showItems', category_id = category_id))
	else:
		return render_template('deleteItem.html', category_id = category_id, item = item)

@app.route('/catalog/<int:category_id>/item/JSON')
def categoryItemsJSON(category_id):
	items = session.query(Item).filter_by(category_id = category_id).all()
	return jsonify(CategoryItems = [i.serialize for i in items])

@app.route('/catalog/JSON/')
def catalogJSON():
	all_items = session.query(Category, Item).filter(Category.id == Item.category_id).all()
	return jsonify(Categories = [dict(i[0].serialize, 
								**{"items":i[1].serialize}) for i in all_items])

@app.route('/users/JSON')
def userJSON():
	users = session.query(User).all()
	return jsonify(Users = [u.serialize for u in users])

@app.route('/login/')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE = state)

@app.route('/gconnect', methods = ['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	code =request.data
	print code

	#upgrade the authorization code into a credential object
	try:
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = '')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)

		print "<<<>>>> Got credentials"
		print credentials
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		request.headers['Content-Type'] = 'application/json'
		return response

	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	print "<<<<<access_token>>>>"
	print result.get('error')

	#Check if there is error with the access token
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	#Verify if the access token is used for the intended user
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's User Id does not math given user Id"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's User Id does not match App's Client ID"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	#Check to see if user is already logged in
	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	#Store the access token in the session for later use
	login_session['access_token'] = credentials.access_token
	print "Access token:<<<<<<<<<<<<<<<"
	print login_session['access_token']
	login_session['gplus_id'] = gplus_id

	#Get user info
	userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
	params = {'access_token':credentials.access_token, 'alt':'json'}
	answer = requests.get(userinfo_url, params = params)
	data = json.loads(answer.text)

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
	print login_session['email']
	login_session['provider'] = 'google'

	user_id = getUserID(login_session)
	if user_id == None:
		print "No such user. Creating one!"
		user_id = createUser(login_session)
	login_session['user_id'] = user_id
	print "<<<<>>> Getting user id %d " % user_id

	output = ''
	output += '<h1>Welcome '
	output += login_session['username']
	output += '!</h1>'
	#output += '<img src = "'
	#output += login_session['picture']
	#output += ('" style = "width: 300px; height:200px; border-radius: 150px; '
	#			'-webkit-border-radius: 150px; -moz-border-radius: 150px;">')
	#flash('You are now logged in as %s ' % login_session['username'])
	print "Here is the output" + output

	return output

@app.route('/fbconnect', methods = ['POST'])
def fbconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	access_token = request.data

	#Exchange short lived client token with long lived server side token
	app_id = json.loads(open('fb_client_secrets.json','r').read())['web']['app_id']
	app_secret = json.loads(open('fb_client_secrets.json','r').read())['web']['app_secret']
	print "<<<>>>>>FB app id and secret"
	print app_id
	print app_secret
	url = ('https://graph.facebook.com/oauth/access_token?'
			'grant_type=fb_exchange_token&client_id=%s'
			'&client_secret=%s&fb_exchange_token=%s')%(app_id, app_secret, access_token)
	h = httplib2.Http()
	result = h.request(url,'GET')[1]
	print result

	#Strip expired tag from access token
	token = result.split('&')[0]
	print token
	login_session['access_token'] = token.split('=')[1]

	#Use token to get user info through API
	#FB latest version requires requested fields!!!
	url = "https://graph.facebook.com/v2.4/me?%s&fields=name,id,email" % token
	print url
	h = httplib2.Http()
	result = h.request(url, 'GET')[1]
	print result
	data = json.loads(result)
	print "Getting from FB___________"
	print data

	#Check to see if user is already logged in
	stored_facebook_id = login_session.get('facebook_id')
	stored_token = login_session.get('access_token')
	if stored_token is not None and stored_facebook_id == data['id']:
		response = make_response(json.dumps('User is already connected'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	#Set up login_session
	login_session['provider'] = 'facebook'
	login_session['username'] = data['name']
	login_session['email'] = data.get('email')
	login_session['facebook_id'] = data['id']

	#Separate API call to get picture
	url = "https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height-200&width=200"%token
	h = httplib2.Http()
	result = h.request(url, 'GET')[1]
	data = json.loads(result)
	print data
	if 'data' in data:
		if 'url' in data['data']:
			login_session['picture'] = data['data']['url']
			print login_session['picture']

	user_id = getUserID(login_session)

	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	if 'picture' in login_session:
	    output += '<img src="'
	    output += login_session['picture']
	    output += (' " style = "width: 300px; '
	    			'height: 200 px; border-radius: 150px; '
	    			'-webkit-border-radius: 150px; -moz-border-radius: 150px;"> ')
	flash("you are now logged in as %s"%login_session['username'])
	return output

@app.route('/logout')
def disconnect():
	if 'provider' in login_session:
		if login_session['provider'] == 'google':
			flash('Disconnecting from Google...')
			gdisconnect()
		if login_session['provider'] == 'facebook':
			fbdisconnect()

		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['user_id']
		del login_session['provider']
		print "being logged out"
		flash('You have successfully logged out.')
	else:
		print "why directed here?"
		flash('You are not logged in.')
	return redirect(url_for('showCatalog'))

@app.route('/gdisconnect/')
def gdisconnect():
	#Only discoonnect a connected user
	access_token = login_session.get('access_token')
	print access_token
	if access_token is None:
		response = make_response(json.dumps('Current user is not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	print result

	if result['status'] == '200':
		#reset the user's sessiion
		del login_session['access_token']
		del login_session['gplus_id']

		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Failed to revoke token for the user.'), 400)
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/fbdisconnect/')
def fbdisconnect():
	facebook_id = login_session['facebook_id']
	access_token = login_session['access_token']

	url = ('https://graph.facebook.com/%s/'
		'permissions?access_token=%s') % (facebook_id, access_token)
	h = httplib2.Http()
	result = h.request(url,'DELETE')[1]
	print result
	del login_session['facebook_id']
	del login_session['access_token']

	return "You are logged out."

if __name__ == '__main__':
	app.debug = True
	app.secret_key = "some_exe_secret"
	app.run(host = '0.0.0.0', port = 5000)