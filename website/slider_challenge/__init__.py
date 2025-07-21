# website/slider_challenge/__init__.py
from flask import Blueprint

slider_challenge = Blueprint('slider_challenge', __name__, template_folder='templates')

from . import slider_challenge
