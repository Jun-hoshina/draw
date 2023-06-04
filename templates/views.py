from flask import render_template, flash, Blueprint

main = Blueprint("main", __name__)

@main.route("/")
def index_view():
    return render_template("index.html")

