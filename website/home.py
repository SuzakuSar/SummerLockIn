from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/')
def home_Page():
    return render_template('home.html')