# ============= FILE STRUCTURE =============
# Add this to your website/ directory:
# 
# website/
# ├── prank_helper/
# │   ├── __init__.py
# │   ├── prank_helper.py
# │   └── templates/
# │       └── prank_helper.html

# ============= website/prank_helper/__init__.py =============

# ============= website/prank_helper/prank_helper.py =============
from flask import Blueprint, render_template, jsonify

# Create blueprint with template folder
prank_helper = Blueprint('prank_helper', __name__, template_folder='templates')

@prank_helper.route('/')
def index():
    """Main prank helper page"""
    return render_template('prank_helper.html')

@prank_helper.route('/api/reset')
def reset_prank():
    """API endpoint to reset prank state (if needed for future features)"""
    return jsonify({
        'status': 'success',
        'message': 'Prank reset successfully'
    })

# ============= REGISTER IN website/__init__.py =============
# Add this to your existing create_app() function:

def create_app():
    app = Flask(__name__)
    app.secret_key = 'shh_its_a_secret'
    
    # Import blueprints
    from .home import home
    from .helloWorld import helloWorld
    from .clicker_game.clicker_game import clicker_game
    from .random_jokes.random_jokes import random_jokes
    from .guessing_game.guessing_game import guessing_game
    from .hangman import hangman
    from .time_predict.time_predict import time_predict  # if you have this
    from .space_memory.space_memory import space_memory  # if you have this
    from .prank_helper.prank_helper import prank_helper  # <-- ADD THIS LINE
    
    # Register blueprints
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(helloWorld, url_prefix='/')
    app.register_blueprint(clicker_game, url_prefix='/clickergame')
    app.register_blueprint(random_jokes, url_prefix='/randomjokes')
    app.register_blueprint(guessing_game, url_prefix='/guessinggame')
    app.register_blueprint(hangman, url_prefix='/hangman')
    app.register_blueprint(time_predict, url_prefix='/timepredict')  # if you have this
    app.register_blueprint(space_memory, url_prefix='/spacememory')  # if you have this
    app.register_blueprint(prank_helper, url_prefix='/prankhelper')  # <-- ADD THIS LINE
    
    return app