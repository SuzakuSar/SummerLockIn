# guessing_game_blueprint.py

from flask import Blueprint, render_template, request, session, redirect, url_for
import random

# Create a Blueprint named 'guessing_game_bp'
# First parameter is the blueprint's name
# Second parameter is the import name (usually __name__)
# url_prefix will be prepended to all routes in this blueprint
guessing_game_bp = Blueprint('guessing_game_bp', __name__)

@guessing_game_bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route handler for the guessing game blueprint.
    Handles all game states and logic in one function.
    """
    # Initialize the game or reset it when requested
    # 'initialized' is used to track if the game has been set up in the session
    if 'initialized' not in session or request.form.get('reset') == 'true':
        # Set up initial game state in the session
        session['initialized'] = True  # Mark game as initialized
        session['game_started'] = False  # Game not yet started
        session['level_chosen'] = False  # Level not yet chosen
        session['attempts'] = []  # Empty list to track attempts
        session['num_of_attempts'] = 0  # Counter for number of attempts
        # Render the welcome screen
        return render_template('guessing_game/index.html')
    
    # Handle welcome screen submission - move to level selection
    if not session.get('game_started') and request.method == 'POST':
        session['game_started'] = True  # Mark game as started
        # Render the level selection screen
        return render_template('guessing_game/level.html')
    
    # Handle difficulty level selection
    if session.get('game_started') and not session.get('level_chosen') and request.method == 'POST':
        level = request.form.get('level')  # Get the selected level from the form
        if level in ['1', '2']:  # Validate level choice
            session['level'] = int(level)  # Store the level in the session
            session['level_chosen'] = True  # Mark level as chosen
            
            # Set up game parameters based on difficulty level
            if session['level'] == 1:  # Normal difficulty
                session['target_number'] = random.randint(0, 20)  # Generate random number 0-20
                session['max_range'] = 20  # Set the max range for validation
            else:  # Hard difficulty
                session['target_number'] = random.randint(0, 30)  # Generate random number 0-30
                session['max_range'] = 30  # Set the max range for validation
            
            # Render the main game screen with initial game state
            return render_template('guessing_game/game.html', 
                                  level=session['level'], 
                                  max_range=session['max_range'],
                                  attempts=session['attempts'],
                                  num_attempts=session['num_of_attempts'])
        else:
            # If invalid level, ask again with error message
            return render_template('guessing_game/level.html', error="Please choose 1 or 2.")
    
    # Handle guess submissions during the game
    if session.get('level_chosen') and request.method == 'POST' and 'guess' in request.form:
        guess_str = request.form.get('guess', '')  # Get the guess from the form
        
        try:
            # Try to convert the guess to an integer
            guess = int(guess_str)
            # Increment attempt counter
            session['num_of_attempts'] += 1
            
            # Add guess to attempts list
            if 'attempts' not in session:
                session['attempts'] = []
            session['attempts'].append(guess)
            
            # Check if the guess is correct
            if guess == session['target_number']:
                result = "correct"
                # Render the result screen with game outcome
                return render_template('guessing_game/result.html',
                                      result=result,
                                      target_number=session['target_number'],
                                      num_attempts=session['num_of_attempts'],
                                      attempts=session['attempts'])
            
            # Validate guess is in range and provide appropriate hint
            if session['level'] == 1 and (guess < 0 or guess > 20):
                hint = "That's not an option dummy. Guess between 0 and 20."
            elif session['level'] == 2 and (guess < 0 or guess > 30):
                hint = "That's not an option dummy. Guess between 0 and 30."
            # Provide hint based on comparison with target number
            elif guess > session['target_number']:
                hint = "Lower"
            else:
                hint = "Higher"
            
            # Render game screen with updated state and hint
            return render_template('guessing_game/game.html', 
                                  level=session['level'], 
                                  max_range=session['max_range'],
                                  attempts=session['attempts'],
                                  num_attempts=session['num_of_attempts'],
                                  hint=hint)
            
        except ValueError:
            # Handle non-numeric input with appropriate error message
            return render_template('guessing_game/game.html', 
                                  level=session['level'], 
                                  max_range=session['max_range'],
                                  attempts=session['attempts'],
                                  num_attempts=session['num_of_attempts'],
                                  hint="Try typing in a number")
    
    # Default behavior: redirect based on current game state
    if session.get('level_chosen'):
        # If level is chosen but not handling a POST request, show the game screen
        return render_template('guessing_game/game.html', 
                              level=session['level'], 
                              max_range=session['max_range'],
                              attempts=session['attempts'],
                              num_attempts=session['num_of_attempts'])
    elif session.get('game_started'):
        # If game started but level not chosen, show level selection
        return render_template('guessing_game/level.html')
    else:
        # Default to welcome screen
        return render_template('guessing_game/index.html')