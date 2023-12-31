from config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from datetime import datetime, timedelta
from sqlalchemy.sql import func

from sqlalchemy_serializer import SerializerMixin
import re

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ('-wedding','-todos', '-guests')

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    wedding = db.relationship('Wedding', uselist=False, backref='user' )
    todos = db.relationship('ToDo', backref='user' )
    guests = db.relationship('Guest', backref="user")
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

    

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    wedding_date = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    isAttending = db.Column(db.Boolean )

class ToDo(db.Model, SerializerMixin):
    __tablename__= 'todos'

    id  = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String, nullable=False)
    isDone = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



