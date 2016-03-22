from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc
from database import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def getCategory(category_id):
	return session.query(Category).filter_by(id = category_id).first()

def getAllCategories():
	return session.query(Category).all()

@app.route('/')
@app.route('/catalog/')
def showCatalog():
	categories = session.query(Category).all()
	recentItems = session.query(Category.name, Item).filter(Category.id == Item.category_id).order_by(Item.date_added.desc()).limit(5)
	print recentItems
	flash('Testing flash!')
	return render_template('catalog.html', categories = categories, recentItems = recentItems)


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/item')
def showItems(category_id):
	category = getCategory(category_id = category_id)
	items = session.query(Item).filter_by(category_id = category_id).all()
	return render_template('category.html', category  = category, 
							num_items = len(items), items= items, allow_edit = True)

@app.route('/catalog/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
	c = session.query(Category).filter_by(id = category_id).first()
	i = session.query(Item).filter_by(category_id = category_id, id = item_id).first()
	showPic = False
	if i.picture and len(i.picture) > 0 and i.picture.endswith('jpg'):
		showPic = True

	return render_template('item.html', category = c, item = i, 
							allow_edit = True, showPic = showPic)

@app.route('/catalog/<int:category_id>/new', methods = ['GET', 'POST'])
def addItem(category_id):
	if request.method == 'POST':
		selectedCategory = str(request.form['selectedCategory'])
		print selectedCategory
		new_category_id = session.query(Category).filter_by(name = selectedCategory).first().id
		if new_category_id:
			category_id = new_category_id
			print category_id

		newItem = Item(name = request.form['itemName'], 
						description = request.form['itemDescription'],
						category_id = category_id, picture = request.form['imageFile'])
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

@app.route('/login/')
def showLogin():
	return "Login page"

@app.route('/gconnect/', methods = ['POST'])
def gconnect():
	return "Connecting through Google+"

@app.route('/fbconnect/', methods = ['POST'])
def fbconnect():
	return "Connecting through FB"

@app.route('/logout')
def disconnect():
	return "disconnect"

@app.route('/gdisconnect/')
def gdisconnect():
	return "Disconnecting from Google"

@app.route('/fbdisconnect/')
def fbdisconnect():
	return "Disconnecting from FB"

if __name__ == '__main__':
	app.debug = True
	app.secret_key = "some_exe_secret"
	app.run(host = '0.0.0.0', port = 5000)