from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

category1 = Category(name = 'Hiking Boots')

session.add(category1)
session.commit()

item1_hb = Item(name = 'Asolo Neutron', 
				description = 'Waterproof, moisture wicking, Vibram outsole for excellent grip and shock absorbtion',
				price = '180',
				picture = 'asolo.jpg',
				category = category1)

session.add(item1_hb)
session.commit()

item2_hb = Item(name = 'Hanwag Xerro', 
	description = 'Waterproof, moisture wicking, Rubber toe cap for durability, HANWAG IceGrip lugged rubber outsole',
	price = '150',
	picture = 'hanwag.jpg',
	category = category1)

session.add(item2_hb)
session.commit()

category2 = Category(name = 'Hiking Poles')

session.add(category2)
session.commit()

item1_hb = Item(name = 'Black Diamond Ultra Distance Z Pole', 
				description = 'Three-section Z-Pole folding design with speed cone deployment',
				price = '120',
				picture = 'bdz.jpg',
				category = category2)

session.add(item1_hb)
session.commit()

item2_hb = Item(name = 'Komperdell Carbon Approach Vario 4 Trekking Poles', 
	description = ('Ultralight carbon fiber shaft is incredibly strong, '
					'Power Lock II locking mechanism provides quick and secure height adjustment'),
	price = '150',
	picture = 'komperdell.jpg',
	category = category2)

session.add(item2_hb)
session.commit()

category3 = Category(name = 'Backpacks')

session.add(category2)
session.commit()

item1_hb = Item(name = 'Osprey Exos', 
				description = ('Ultralight and supportive, '
								'this pack offers the best of both worlds; '
								'its airy suspension is both light and comfortable '
								'for superlight backpacking and thru-hiking'),
				price = '190',
				picture = 'osprey.jpg',
				category = category3)

session.add(item1_hb)
session.commit()

item2_hb = Item(name = 'Kelty Catalyst', 
	description = ('Loaded-up with exterior stretch pockets, '
					'a side-access sleeping bag compartment and top and panel loading access, '
					'this multiday pack keeps your gear comfortably stowed and easy to access on the trail.'),
	price = '179.99',
	picture = 'kelty.jpg',
	category = category3)

session.add(item2_hb)
session.commit()

category4 = Category(name = 'Hiking Socks')

session.add(category4)
session.commit()

item1_hb = Item(name = 'Smartwool Hiking Socks', 
				description = ('These no-itch SmartWool hiking socks maintain softness '
								'and shape through seasons of wear and washing'),
				price = '12',
				picture = 'smartwool.jpg',
				category = category4)

session.add(item1_hb)
session.commit()

item2_hb = Item(name = 'Darn Tough CoolMax Micro Crew Cushion Socks', 
	description = ('Made in Vermont with legendary Darn Tough construction and '
					'performance fit to keep socks in place all day, '
					'with no slipping, bunching, blisters or hot spots'),
	price = '10',
	picture = 'darn.jpg',
	category = category4)

session.add(item2_hb)
session.commit()