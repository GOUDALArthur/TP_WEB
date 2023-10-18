from .app import app, db
from flask import render_template, url_for, redirect
from .models import get_sample, get_author, get_book, Author, book_by_author, max_id_author
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators = [DataRequired()])

class AddAuthorForm(FlaskForm) :
    id = HiddenField('id')
    name = StringField("Entre le nom du nouvelle auteur", validators=[DataRequired()])

@app.route("/")
def home():
    return render_template(
        "home.html",
        title = "Hello World",
        books = get_sample()
    )

@app.route("/detail/<id>")
def detail(id):
    book = get_book(id)
    return render_template(
        "detail.html",
        book = book
    )

@app.route("/edit/author/<int:id>")
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id = a.id, name = a.name)
    return render_template(
        "edit-author.html",
        author=a, form=f
    )

@app.route("/save/author/", methods =("POST" ,))
def save_author ():
    a = None
    f = AuthorForm ()
    if f. validate_on_submit ():
        id = int(f.id.data)
        a = get_author (id)
        a.name = f.name.data
        db.session.commit ()
        return redirect(url_for('author', id=a.id))
    a = get_author (int(f.id.data ))
    return render_template (
        "edit -author.html",
        author=a, form=f)

@app.route("/author/<int:id>")
def author(id) :
    books = book_by_author(id)
    author = get_author(id)
    return render_template(
        "author.html",
        author = author,
        books = books
    )

@app.route("/add/author/")
def add_author() :
    max = max_id_author() + 1
    f = AddAuthorForm(id=max, name = "John")
    return render_template(
        "add-author.html",
        form=f
    )

@app.route("/save/add/author/", methods=("POST",))
def save_add_author() :
    a = None
    f = AddAuthorForm()
    if f.validate_on_submit() :
        a = Author(name=f.name.data)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('author', id=a.id))
    a = get_author(int(f.id.data))
    return render_template(
        "add-author.html",
        author=a, form=f
    )