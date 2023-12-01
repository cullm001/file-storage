from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import *
import random

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(150), unique = True)
    file_size = db.Column(db.Integer)
    file_size_display = db.Column(db.String(10))
    date = db.Column(db.String(150), default=datetime.now().strftime("%B %d, %Y %I:%M %p"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    files = db.relationship('File')