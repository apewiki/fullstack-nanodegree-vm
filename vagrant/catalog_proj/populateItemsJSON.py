import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def cleanup():
	for c in session.query(Category):
		session.delete(c)
		session.commit()

	for i in session.query(Item):
		session.delete(i)
		session.commit()

	for u in session.query(User):
		session.delete(u)
		session.commit()


def populate():
	with open('catalog.json') as data_file:
		data = json.load(data_file)
		for c in data['Categories']:
			print c
			print c['id']
			e = session.query(Category).filter_by(id=c['id']).first()
			print e
			if e is None:
				category = Category(id=c['id'], name=c['name'], user_id=c['user_id'])
				session.add(category)
				session.commit()
			i=c['items']
			item = Item(
				id=i['id'], name=i['name'], description=i['description'],
				price=i['price'], picture=i['picture'],
				user_id=i['user_id'], category_id=c['id'], date_added=datetime.strptime(
					i['date_added'], '%a, %d %b %Y %H:%M:%S %Z'))
			session.add(item)
			session.commit()


def setup_users():
	with open('users.json') as data_file:
		data = json.load(data_file)
		for u in data['Users']:
			print u['id']
			user = User(id=u['id'], name=u['name'], email=u['email'], picture=u['picture'])
			session.add(user)
			session.commit()

cleanup()
setup_users()
populate()

