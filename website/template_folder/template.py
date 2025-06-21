from flask import Blueprint, render_template


example_name = Blueprint('example_name', __name__, template_folder='templates')

@example_name.route('/')
def index():
    return render_template('template.html')