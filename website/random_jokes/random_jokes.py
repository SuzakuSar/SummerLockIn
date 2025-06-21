from flask import Flask, Blueprint, render_template, jsonify
from website.random_jokes.joke_list import jokes
import random


random_jokes = Blueprint('random_jokes', __name__, template_folder='templates')

def get_joke():
    return random.choice(jokes)

@random_jokes.route('/')
def index():
    joke = get_joke()
    # Render the index.html template and pass the joke to it
    return render_template('random_jokes.html', joke=joke)

@random_jokes.route('/api/joke', methods=['GET'])
def api_joke():
    joke = get_joke()   
        # Return the joke as JSON so JavaScript can use it
    return jsonify({'joke': joke})