"""Data models for Flask Cafe"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = 'cities'

    code = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    state = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return f'<City code={self.code}, name={self.name}, state={self.state}>'

    @classmethod
    def get_city_codes(cls):
        """Get a list of city codes"""

        return [(city.code, city.name) for city in City.query.order_by('name').all()]


class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = 'cafes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    city_code = db.Column(db.Text, db.ForeignKey(
                'cities.code'), nullable=False)
    image_url = db.Column(
                db.Text, nullable=False,
                default="/static/images/default-cafe.jpg")
    city = db.relationship("City", backref='cafes')

    liking_users = db.relationship('User', secondary='likes')

    def __repr__(self):
        return f'<Cafe id={self.id} name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f'{city.name}, {city.state}'


class User(db.Model):
    """User information."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(
        db.Text, nullable=False, default="/static/images/default-pic.png")
    hashed_password = db.Column(db.Text, nullable=False)
 
    liked_cafes = db.relationship('Cafe', secondary='likes')

    def get_full_name(self):
        """Return full name of user"""
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def register(
        cls, username, email, first_name, last_name, description, 
            password, image_url=None, admin=False):
        """Register user with hashed password."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed password
        user = cls(
                username=username, admin=admin, email=email, 
                first_name=first_name, last_name=last_name, 
                description=description, hashed_password=hashed_utf8,
                image_url=image_url)
        
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct.
        Return user if valid; else return False.
        """
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.hashed_password, password):
            # return user instance
            return u
        else:
            return False


class Like(db.Model):
    """Likes for users liking cafes."""

    __tablename__ = 'likes'

    user_id = db.Column(
            db.Integer, db.ForeignKey('users.id'), primary_key=True)
    cafe_id = db.Column(
            db.Integer, db.ForeignKey('cafes.id'), primary_key=True)


def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)
