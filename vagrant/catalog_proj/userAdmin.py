from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

user1 = session.query(User).filter_by(email = 'a1p9e86@gmail.com').first()
if user1:
	session.delete(user1)
user2 = session.query(User).filter_by(email = 'uccandreamc@gmail.com').first()
if user2:
	session.delete(user2)
session.commit()

for i in session.query(Item).filter_by(user_id = 3).all():
	i.user_id = 2
	session.commit()

for i in session.query(Item).filter(Item.user_id == None).all():
	i.user_id = 1
	session.commit()
