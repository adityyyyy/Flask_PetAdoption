from datetime import datetime
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.user)

    


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    species = db.Column(db.String(64))
    breed = db.Column(db.String(64))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(8))
    description = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Pet {}>'.format(self.name)

