from .app import app
from flask import render_template
from .models import get_sample

@app.route("/")
def home():
    return render_template(
        "home.html",
        title = "Hello World",
        books = get_sample()
    )