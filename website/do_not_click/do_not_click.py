# File: website/do_not_click/do_not_click.py
from flask import Blueprint, render_template, abort

# Create blueprint with template folder
do_not_click = Blueprint('do_not_click', __name__, template_folder='templates')

@do_not_click.route('/')
def index():
    """Main page with the big red button that shouldn't be clicked."""
    return render_template('do_not_click.html')

@do_not_click.route('/clicked')
def clicked():
    """Route that triggers when the forbidden button is clicked - sends to 404."""
    abort(404)

@do_not_click.route('/warning')
def warning():
    """Optional warning page that appears before the 404 (for dramatic effect)."""
    return render_template('warning.html')