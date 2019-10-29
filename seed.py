"""Initial data."""
from config import DATABASE_URL
from models import City, Cafe, User, db, connect_db
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.drop_all()
db.create_all()


#######################################
# add cities

sf = City(code='sf', name='San Francisco', state='CA')
berk = City(code='berk', name='Berkeley', state='CA')
oak = City(code='oak', name='Oakland', state='CA')

db.session.add_all([sf, berk, oak])
db.session.commit()


#######################################
# add cafes

c1 = Cafe(
    name="Bernie's Cafe",
    description='Serving locals in Noe Valley. A great place to sit and code'
        ' and code.',
    address="3966 24th St",
    city_code='sf',
    url='https://www.yelp.com/biz/bernies-san-francisco',
    image_url='https://s3-media4.fl.yelpcdn.com/bphoto/bVCa2JefOCqxQsM6yWrC-A/o.jpg'
)

c2 = Cafe(
    name='Perch Coffee',
    description='Hip and sleek place to get cardamom lattés when biking'
        ' around Oakland.',
    address='440 Grand Ave',
    city_code='oak',
    url='https://perchoffee.com',
    image_url='https://s3-media4.fl.yelpcdn.com/bphoto/0vhzcgkzIUIEPIyL2rF_YQ/o.jpg',
)

c3 = Cafe(
    name='Cafe du Soleil',
    description='Pastries, Parisian-inspired fare, coffee and wine served'
        ' in a corner bistro.',
    address='200 Fillmore St',
    city_code='sf',
    url='http://cafe-du-soleil.cafes-city.com/',
    image_url='https://s3-media2.fl.yelpcdn.com/bphoto/l6oeG-xz1sJ5PWDJEG-zHg/o.jpg',
)

c4 = Cafe(
    name='Victory Point Cafe',
    description="Berkeley's board game cafe plus craft coffee and beer.",
    address='1797 Shattuck Ave',
    city_code='berk',
    url='https://www.victorypointcafe.com/',
    image_url='https://s3-media1.fl.yelpcdn.com/bphoto/oZHI0cmzCnUDMP7WPAjEEw/o.jpg',
)

db.session.add_all([c1, c2, c3, c4])
db.session.commit()


#######################################
# add users

ua = User.register(
    username="admin",
    first_name="Addie",
    last_name="MacAdmin",
    description="I am the very model of the modern model administrator.",
    email="admin@test.com",
    password="secret",
    admin=True,
)

u1 = User.register(
    username="test",
    first_name="Testy",
    last_name="MacTest",
    description="I am the ultimate representative user.",
    email="test@test.com",
    password="secret",
)

db.session.add_all([u1, ua])
db.session.commit()


#######################################
# add likes

u1.liked_cafes.append(c1)
u1.liked_cafes.append(c2)
ua.liked_cafes.append(c1)

db.session.commit()


#######################################
# cafe maps

c1.save_map()
c2.save_map()
c3.save_map()
c4.save_map()

#db.session.commit()
