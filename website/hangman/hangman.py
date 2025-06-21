from flask import Blueprint, render_template, request, redirect, url_for, session
import random
import string

# Create blueprint with template folder
hangman_blueprint = Blueprint('hangman', __name__, template_folder='templates')

# Import your existing files
from website.hangman.words import words
from website.hangman.hangman_visual import lives_visual_dict

# Define difficulty scales (from your original code)
difficulty_scale_1 = [3, 4, 5, 6]  # Easy
difficulty_scale_2 = [7, 8, 9, 10] # Hard

def get_word(words_list, difficulty):
    """Get a random word based on difficulty level"""
    word = random.choice(words_list)
    scale = difficulty_scale_1 if difficulty == 1 else difficulty_scale_2
    
    while '-' in word or ' ' in word or len(word) not in scale:
        word = random.choice(words_list)
    
    return word.upper()

@hangman_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Hangman welcome screen"""
    # Reset game if requested
    if request.method == 'POST' and 'reset' in request.form:
        session.pop('hangman_word', None)
        session.pop('hangman_used_letters', None)
        session.pop('hangman_lives', None)
        session.pop('hangman_message', None)
        session.pop('hangman_difficulty', None)
    
    # Handle difficulty selection
    if request.method == 'POST' and 'difficulty' in request.form:
        difficulty = int(request.form['difficulty'])
        if difficulty in [1, 2]:
            # Get a random word based on difficulty
            word = get_word(words, difficulty)
            
            # Initialize game state in session with unique keys
            session['hangman_difficulty'] = difficulty
            session['hangman_word'] = word
            session['hangman_used_letters'] = []
            session['hangman_lives'] = 7  # 7 lives to match your visual dict
            session['hangman_message'] = "Game started! Guess a letter."
            
            # Redirect to game page
            return redirect(url_for('hangman.game'))
    
    # Render the welcome template
    return render_template('hangman_index.html')

@hangman_blueprint.route('/game', methods=['GET', 'POST'])
def game():
    """Main game screen"""
    # Redirect to welcome screen if game not started
    if 'hangman_word' not in session:
        return redirect(url_for('hangman.index'))
    
    # Get game state from session
    word = session['hangman_word']
    used_letters = set(session['hangman_used_letters'])
    lives = session['hangman_lives']
    message = session.get('hangman_message', '')
    
    # Handle letter guess
    if request.method == 'POST' and 'letter' in request.form:
        letter = request.form['letter'].upper()
        alphabet = set(string.ascii_uppercase)
        
        # Valid letter that hasn't been used
        if letter in alphabet and letter not in used_letters:
            used_letters.add(letter)
            session['hangman_used_letters'] = list(used_letters)
            
            # Check if letter is in the word
            if letter in word:
                session['hangman_message'] = f"Good job! '{letter}' is in the word."
            else:
                session['hangman_lives'] -= 1
                session['hangman_message'] = f"Sorry, '{letter}' is not in the word."
        
        # Letter already used
        elif letter in used_letters:
            session['hangman_message'] = f"You've already guessed '{letter}'. Try another letter."
        
        # Invalid input
        else:
            session['hangman_message'] = "That's not a valid letter. Try again."
        
        return redirect(url_for('hangman.game'))
    
    # Check win/loss conditions
    word_letters = set(word)
    remaining_letters = word_letters - used_letters
    lives = session['hangman_lives']
    
    # Create display word with dashes for unguessed letters
    display_word = ''.join([letter if letter in used_letters else '_' for letter in word])
    
    # Get the correct hangman picture from your visual dictionary
    hangman_pic = lives_visual_dict[lives]
    
    # Generate the game screen with a distinctive look
    game_over = False
    won = False
    
    if lives <= 0:
        game_over = True
        won = False
        message = f"Game over! The word was '{word}'."
    elif not remaining_letters:
        game_over = True
        won = True
        message = f"Congratulations! You guessed the word '{word}'!"
    
    # Render the game template
    return render_template('hangman_game.html',
                          word=word if game_over else display_word,
                          visual=hangman_pic,
                          used_letters=sorted(used_letters),
                          lives=lives,
                          message=message,
                          game_over=game_over,
                          won=won)