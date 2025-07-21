# website/shell_game/shell_game.py
from flask import Blueprint, render_template, request, session, jsonify
import random

shell_game = Blueprint('shell_game', __name__, template_folder='templates')

@shell_game.route('/')
def index():
    """Main shell game page"""
    # Initialize session variables if not present
    if 'shell_game_score' not in session:
        session['shell_game_score'] = 0
    if 'shell_game_total_games' not in session:
        session['shell_game_total_games'] = 0
    if 'shell_game_streak' not in session:
        session['shell_game_streak'] = 0
    
    return render_template('shell_game.html')

@shell_game.route('/new_game', methods=['POST'])
def new_game():
    """Start a new shell game round"""
    # Randomly place the ball under one of the three buckets (0, 1, or 2)
    correct_bucket = random.randint(0, 2)
    
    # Store the correct answer in session
    session['shell_game_current_answer'] = correct_bucket
    session['shell_game_game_active'] = True
    
    # Generate shuffle sequence for animation
    shuffle_moves = []
    positions = [0, 1, 2]  # Track current positions of buckets
    
    # Create 8-12 random swaps for realistic shuffling
    num_swaps = random.randint(8, 12)
    for _ in range(num_swaps):
        # Pick two random positions to swap
        pos1, pos2 = random.sample(range(3), 2)
        shuffle_moves.append([pos1, pos2])
        # Update positions for tracking
        positions[pos1], positions[pos2] = positions[pos2], positions[pos1]
    
    return jsonify({
        'success': True,
        'correct_bucket': correct_bucket,
        'shuffle_sequence': shuffle_moves
    })

@shell_game.route('/make_guess', methods=['POST'])
def make_guess():
    """Process the player's guess"""
    if not session.get('shell_game_game_active', False):
        return jsonify({'error': 'No active game'})
    
    data = request.get_json()
    player_guess = data.get('guess')
    correct_answer = session.get('shell_game_current_answer')
    
    if player_guess is None or correct_answer is None:
        return jsonify({'error': 'Invalid guess or game state'})
    
    # Check if guess is correct
    is_correct = (player_guess == correct_answer)
    
    # Update session statistics
    session['shell_game_total_games'] += 1
    
    if is_correct:
        session['shell_game_score'] += 1
        session['shell_game_streak'] += 1
    else:
        session['shell_game_streak'] = 0
    
    # Mark game as finished
    session['shell_game_game_active'] = False
    
    return jsonify({
        'correct': is_correct,
        'correct_bucket': correct_answer,
        'score': session['shell_game_score'],
        'total_games': session['shell_game_total_games'],
        'streak': session['shell_game_streak'],
        'accuracy': round((session['shell_game_score'] / session['shell_game_total_games']) * 100, 1)
    })

@shell_game.route('/reset_stats', methods=['POST'])
def reset_stats():
    """Reset all game statistics"""
    session['shell_game_score'] = 0
    session['shell_game_total_games'] = 0
    session['shell_game_streak'] = 0
    session['shell_game_game_active'] = False
    
    return jsonify({'success': True})