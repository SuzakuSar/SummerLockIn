from flask import Flask, Blueprint, render_template, jsonify
from website.jokeList import jokes
import random


randomJokes = Blueprint('randomJokes', __name__)

def get_Joke():
    return random.choice(jokes)

@randomJokes.route('/')
def random_Jokes():
    joke = get_Joke()
    # Render the index.html template and pass the joke to it
    return render_template('randomJokes.html', joke=joke)

@randomJokes.route('/api/joke', methods=['GET'])
def api_Joke():
    joke = get_Joke()
        # Return the joke as JSON so JavaScript can use it
    return jsonify({'joke': joke})