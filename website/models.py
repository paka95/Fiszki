from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    sets = db.relationship('Set', backref='user', passive_deletes=True)


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    flashcards = db.relationship('Flashcard', backref='set', passive_deletes=True)


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstside = db.Column(db.Text, nullable=False)
    secondside = db.Column(db.Text, nullable=False)
    of_set = db.Column(db.Integer, db.ForeignKey('set.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

