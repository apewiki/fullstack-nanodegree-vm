from sqlalchemy import Column, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	email = Column(String(250), nullable = False)
	picture = Column(String(250))

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'email': self.email,
			'picture': self.picture
		}

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	user_id = Column(Integer, ForeignKey('user.id'))
	User = relationship(User)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'user_id': self.user_id
		}



class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	description = Column(String(500))
	price = Column(String(50))
	picture = Column(String(250))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	date_added = Column(DateTime, default = func.now())

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'price': self.price,
			'picture': self.picture,
			'category_id': self.category_id,
			'user_id': self.user_id,
			'date_added': self.date_added
		}

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
