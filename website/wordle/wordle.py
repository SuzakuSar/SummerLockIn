# website/wordle/wordle.py
from flask import Blueprint, render_template, request, jsonify, session
import random

wordle = Blueprint('wordle', __name__, template_folder='templates')

# Simple word list - keeping it small and manageable
WORD_LIST = [
    'ABOUT', 'ABOVE', 'ABUSE', 'ACTOR', 'ACUTE', 'ADMIT', 'ADOPT', 'ADULT', 'AFTER', 'AGAIN',
    'AGENT', 'AGREE', 'AHEAD', 'ALARM', 'ALBUM', 'ALERT', 'ALIEN', 'ALIGN', 'ALIKE', 'ALIVE',
    'ALLOW', 'ALONE', 'ALONG', 'ALTER', 'AMONG', 'ANGER', 'ANGLE', 'ANGRY', 'APART', 'APPLE',
    'APPLY', 'ARENA', 'ARGUE', 'ARISE', 'ARRAY', 'ASIDE', 'ASSET', 'AUDIO', 'AUDIT', 'AVOID',
    'AWAKE', 'AWARD', 'AWARE', 'BADLY', 'BASIC', 'BEACH', 'BEGAN', 'BEGIN', 'BEING', 'BELOW',
    'BENCH', 'BILLY', 'BIRTH', 'BLACK', 'BLAME', 'BLANK', 'BLAST', 'BLIND', 'BLOCK', 'BLOOD',
    'BOARD', 'BOOST', 'BOOTH', 'BOUND', 'BRAIN', 'BRAND', 'BRASS', 'BRAVE', 'BREAD', 'BREAK',
    'BREED', 'BRIEF', 'BRING', 'BROAD', 'BROKE', 'BROWN', 'BUILD', 'BUILT', 'BUYER', 'CABLE'
]

def get_random_word():
    """Get a random word from the word list"""
    return random.choice(WORD_LIST)

def check_guess(guess, target):
    """
    Check guess against target word and return result
    Returns list of tuples: (letter, status)
    Status: 'correct', 'present', 'absent'
    """
    guess = guess.upper()
    target = target.upper()
    result = []
    
    # Count letters in target for proper yellow/green logic
    target_counts = {}
    for letter in target:
        target_counts[letter] = target_counts.get(letter, 0) + 1
    
    # First pass - mark correct positions (green)
    guess_result = [''] * 5
    remaining_target_counts = target_counts.copy()
    
    for i in range(5):
        if guess[i] == target[i]:
            guess_result[i] = 'correct'
            remaining_target_counts[guess[i]] -= 1
    
    # Second pass - mark present but wrong position (yellow) and absent (gray)
    for i in range(5):
        if guess_result[i] == '':  # Not already marked as correct
            letter = guess[i]
            if letter in remaining_target_counts and remaining_target_counts[letter] > 0:
                guess_result[i] = 'present'
                remaining_target_counts[letter] -= 1
            else:
                guess_result[i] = 'absent'
    
    # Return as list of (letter, status) tuples
    return [(guess[i], guess_result[i]) for i in range(5)]

@wordle.route('/')
def index():
    """Main Wordle game page"""
    # Initialize new game if needed
    if 'wordle_target_word' not in session:
        session['wordle_target_word'] = get_random_word()
        session['wordle_guesses'] = []
        session['wordle_game_over'] = False
        session['wordle_won'] = False
    
    return render_template('wordle.html')

@wordle.route('/guess', methods=['POST'])
def make_guess():
    """Process a guess"""
    data = request.get_json()
    guess = data.get('guess', '').upper().strip()
    
    # Validation
    if len(guess) != 5:
        return jsonify({'error': 'Guess must be 5 letters'})
    
    if not guess.isalpha():
        return jsonify({'error': 'Guess must contain only letters'})
    
    if guess not in WORD_LIST:
        return jsonify({'error': 'Not a valid word'})
    
    # Check if game is already over
    if session.get('wordle_game_over', False):
        return jsonify({'error': 'Game is already over'})
    
    # Process the guess
    target_word = session['wordle_target_word']
    result = check_guess(guess, target_word)
    
    # Add to guesses
    if 'wordle_guesses' not in session:
        session['wordle_guesses'] = []
    
    session['wordle_guesses'].append({
        'word': guess,
        'result': result
    })
    
    # Check win condition
    if guess == target_word:
        session['wordle_won'] = True
        session['wordle_game_over'] = True
    
    # Check if out of guesses
    elif len(session['wordle_guesses']) >= 6:
        session['wordle_game_over'] = True
        session['wordle_won'] = False
    
    # Save session
    session.modified = True
    
    return jsonify({
        'result': result,
        'game_over': session['wordle_game_over'],
        'won': session.get('wordle_won', False),
        'target_word': target_word if session['wordle_game_over'] else None,
        'guesses_remaining': 6 - len(session['wordle_guesses'])
    })

@wordle.route('/new-game', methods=['POST'])
def new_game():
    """Start a new game"""
    session['wordle_target_word'] = get_random_word()
    session['wordle_guesses'] = []
    session['wordle_game_over'] = False
    session['wordle_won'] = False
    session.modified = True
    
    return jsonify({'success': True})

@wordle.route('/game-state')
def game_state():
    """Get current game state"""
    return jsonify({
        'guesses': session.get('wordle_guesses', []),
        'game_over': session.get('wordle_game_over', False),
        'won': session.get('wordle_won', False),
        'target_word': session.get('wordle_target_word') if session.get('wordle_game_over', False) else None,
        'guesses_remaining': 6 - len(session.get('wordle_guesses', []))
    })