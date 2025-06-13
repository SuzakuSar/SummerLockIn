from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    #app.config['SECRET_KEY'] = 'lol'

    from .helloWorld import helloWorld

    app.register_blueprint(helloWorld, url_prefix='/')

    return app