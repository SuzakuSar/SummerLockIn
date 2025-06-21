from flask import Blueprint, render_template, request, jsonify, session
# Flask - the main web framework class
# render_template - function to display HTML files
# request - handles incoming data from web browser
# jsonify - converts Python data to JSON format for sending back to browser
# session - stores data for each user's visit (like cookies between page loads)

# Create blueprint with template folder (no URL prefix since it's set in init.py)
clicker_game = Blueprint('clicker_game', __name__, template_folder='templates')

@clicker_game.route('/')
# @clicker_game.route('/') means "when someone visits the homepage of this blueprint"
# This is a decorator - it modifies the function below it
def index():
    # Function name changed to index to avoid name conflict with blueprint

    if 'cookies' not in session:
        # Check if 'cookies' key exists in the user's session
        session['cookies'] = 0
        # If not, create it and set to 0
        # session is like a dictionary that remembers data for each user
    
    return render_template('clicker_game.html')  

@clicker_game.route('/click', methods=['POST'])
# This route only accepts POST requests (not GET)
# POST is used when we're sending data or making changes
def click_cookie():
    # This function runs when someone clicks the cookie
    
    session['cookies'] = session.get('cookies', 0) + 1
    # session.get('cookies', 0) gets the current cookie count
    # If 'cookies' doesn't exist, it returns 0 (the default)
    # We add 1 to it (for the click) and save it back to session
    
    return jsonify({'cookies': session['cookies']})
    # jsonify creates a JSON response like: {"cookies": 5}
    # This gets sent back to the browser's JavaScript