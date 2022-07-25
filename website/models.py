import datetime
from website import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    profpic = db.Column(db.LargeBinary)
    username = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    books = db.relationship("Books")
    suggestions = db.relationship("Suggestions")

    def get_id(self):
        return (self.id)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    pic = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def get_id(self):
        return (self.id)

class Suggestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100))
    date_added = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    bought = db.Column(db.Boolean, default=False)
    pic = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def get_id(self):
        return (self.id)

