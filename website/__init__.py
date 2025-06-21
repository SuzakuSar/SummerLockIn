from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    
    # Import blueprints - now importing from the package, not the specific module
    from .home import home
    from .helloWorld import helloWorld
    from .clicker_game import clicker_game
    from .random_jokes import random_jokes
    from .guessing_game import guessing_game
    
    # Register blueprints
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(helloWorld, url_prefix='/')
    app.register_blueprint(clicker_game, url_prefix='/clickergame')
    app.register_blueprint(random_jokes, url_prefix='/randomjokes')
    app.register_blueprint(guessing_game, url_prefix='/guessinggame')
    
    return app