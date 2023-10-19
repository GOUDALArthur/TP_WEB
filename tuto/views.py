from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import get_sample, get_author, get_book, Author, book_by_author, max_id_author, User
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user , current_user, logout_user, login_required

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators = [DataRequired()])

class AddAuthorForm(FlaskForm) :
    id = HiddenField('id')
    name = StringField("Entre le nom du nouvelle auteur", validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField ()
                              
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

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
@login_required
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
@login_required
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

@app.route("/login/", methods =("GET","POST",))
def login ():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user =f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template (
        "login.html",
        form=f)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))

