from flask import Blueprint

story_generator = Blueprint('story_generator', __name__, template_folder='templates')

from . import story_generator