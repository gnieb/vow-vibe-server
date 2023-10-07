from config import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from flask_bcrypt import bcrypt
from sqlalchemy_serializer import SerializerMixin
import re

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    wedding_id = db.relationship('Wedding', backref='user')

    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed')
    
    @password_hash.setter
    def password_hash(self, password):
        if len(password) < 8:
            raise ValueError("passwords must be more than 7 characters")
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )
    
    @validates('email')
    def validate_email(self, key, address):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+');
        if re.fullmatch(regex, address):
            return address
        raise ValueError("Not a valid email address")

    
class Wedding(db.Model, SerializerMixin):
    __tablename__ = 'weddings'

    serialize_rules = ('-guests','-user.weddings',)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    guests = db.relationship('Guest', backref="wedding")


# class UserWeddingInstance(db.Model, SerializerMixin):
#     __tablename__= "userweddinginstances"

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     wedding_id = db.Column(db.Integer, db.ForeignKey('weddings.id'))

class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    wedding_id = db.Column(db.Integer, db.ForeignKey('weddings.id'))