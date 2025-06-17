from flask import Blueprint, render_template
import time

helloWorld = Blueprint('helloWorld', __name__)

@helloWorld.route('/helloworld/')
def hello_World():
    return render_template('helloWorld.html')

@helloWorld.route('/supworld/')
def sup_World():
    return render_template('supWorld.html')     