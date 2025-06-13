from flask import Blueprint, render_template

helloWorld = Blueprint('helloWorld', __name__)

@helloWorld.route('/')
def hello_World():
    return render_template('helloWorld.html')

@helloWorld.route('/supWorld/')
def sup_World():
    return render_template('supWorld.html')