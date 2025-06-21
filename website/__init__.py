from flask import Flask, render_template

# In website/__init__.py

def create_app():
    app = Flask(__name__)
    
    # Import blueprints
    from .home import home
    from .helloWorld import helloWorld
    from .clicker_game.clicker_game import clicker_game
    from .random_jokes.random_jokes import random_jokes
    from .guessing_game.guessing_game import guessing_game
    from .hangman import hangman  # Import the hangman blueprint
    
    # Register blueprints
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(helloWorld, url_prefix='/')
    app.register_blueprint(clicker_game, url_prefix='/clickergame')
    app.register_blueprint(random_jokes, url_prefix='/randomjokes')
    app.register_blueprint(guessing_game, url_prefix='/guessinggame')
    app.register_blueprint(hangman, url_prefix='/hangman')  # Use a unique URL prefix
    
    return app