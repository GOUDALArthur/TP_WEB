from .app import app
from flask import render_template
from .models import get_sample, get_author, get_book
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators = [DataRequired()])

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