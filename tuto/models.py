from .app import db
from sqlalchemy import *
from flask_login import UserMixin

class Author(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "<Author (%d) %s>" % (self.id, self.name)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer ,db.ForeignKey("author.id"))
    author = db.relationship("Author",
    backref=db.backref("books", lazy="dynamic"))

    def __repr__(self):
        return "<Book (%d) %s>" % (self.id, self.title)

class User(db.Model , UserMixin ):
    username = db.Column(db.String (50) , primary_key =True)
    password = db.Column(db.String (64))

    def get_id(self ):
        return self.username

def get_sample():
    return Book.query.all()

def get_author(id):
    return Author.query.get(id)

def get_book(id):
    return Book.query.get(id)

def book_by_author(id) :
    query = select(Book).where(Book.author_id == id)
    res = db.session.execute(query)
    books = [row[0] for row in res]
    return books

def max_id_author() :
    return db.session.query(func.max(Author.id)).scalar()