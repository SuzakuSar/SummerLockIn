from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    #app.config['SECRET_KEY'] = 'lol'

    from .home import home
    from .helloWorld import helloWorld
    from .guessinNumbers import guessNum

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(helloWorld, url_prefix='/')
    app.register_blueprint(guessNum, url_prefix='/')

    return app