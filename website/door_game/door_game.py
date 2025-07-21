# File: website/door_game/door_game.py
from flask import Blueprint, render_template

door_game = Blueprint('door_game', __name__, template_folder='templates')

@door_game.route('/')
def index():
    """Main door game page"""
    return render_template('door_game.html')