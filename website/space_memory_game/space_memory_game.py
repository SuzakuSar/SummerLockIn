from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
import random

# Create blueprint
space_memory_game = Blueprint('space_memory_game', __name__, template_folder='templates')

@space_memory_game.route('/')
def index():
    """Main game page - shows welcome screen and starts new game"""
    # Initialize game session
    session['space_memory_sequence'] = []
    session['space_memory_player_sequence'] = []
    session['space_memory_current_round'] = 1
    session['space_memory_game_state'] = 'waiting'  # waiting, showing, playing, won, lost
    session['space_memory_score'] = 0
    
    return render_template('space_memory_index.html')

@space_memory_game.route('/game')
def game():
    """Game interface page"""
    # Ensure game session exists
    if 'space_memory_sequence' not in session:
        return redirect(url_for('space_memory_game.index'))
    
    return render_template('space_memory_game.html')

@space_memory_game.route('/api/new-game', methods=['POST'])
def new_game():
    """Start a new game - reset all session data"""
    session['space_memory_sequence'] = []
    session['space_memory_player_sequence'] = []
    session['space_memory_current_round'] = 1
    session['space_memory_game_state'] = 'waiting'
    session['space_memory_score'] = 0
    
    return jsonify({
        'status': 'success',
        'round': 1,
        'sequence': [],
        'game_state': 'waiting'
    })

@space_memory_game.route('/api/next-round', methods=['POST'])
def next_round():
    """Generate next sequence for the current round"""
    # Get current game state
    sequence = session.get('space_memory_sequence', [])
    current_round = session.get('space_memory_current_round', 1)
    
    # Add new random square to sequence (0-8 for 3x3 grid)
    available_squares = [i for i in range(9) if i not in sequence]
    
    if not available_squares:
        # All squares used - player wins!
        session['space_memory_game_state'] = 'won'
        session['space_memory_score'] = current_round * 100
        return jsonify({
            'status': 'won',
            'sequence': sequence,
            'round': current_round,
            'score': session['space_memory_score'],
            'game_state': 'won'
        })
    
    # Add random square from available ones
    new_square = random.choice(available_squares)
    sequence.append(new_square)
    
    # Update session
    session['space_memory_sequence'] = sequence
    session['space_memory_player_sequence'] = []
    session['space_memory_game_state'] = 'showing'
    
    return jsonify({
        'status': 'success',
        'sequence': sequence,
        'round': current_round,
        'game_state': 'showing'
    })

@space_memory_game.route('/api/player-input', methods=['POST'])
def player_input():
    """Handle player square selection"""
    data = request.get_json()
    square_id = data.get('square_id')
    
    # Get current game state
    sequence = session.get('space_memory_sequence', [])
    player_sequence = session.get('space_memory_player_sequence', [])
    current_round = session.get('space_memory_current_round', 1)
    
    # Add player input to their sequence
    player_sequence.append(square_id)
    session['space_memory_player_sequence'] = player_sequence
    
    # Check if input matches expected sequence so far
    if player_sequence[-1] != sequence[len(player_sequence) - 1]:
        # Wrong input - game over
        session['space_memory_game_state'] = 'lost'
        return jsonify({
            'status': 'wrong',
            'correct_sequence': sequence,
            'player_sequence': player_sequence,
            'game_state': 'lost'
        })
    
    # Check if player completed the current sequence
    if len(player_sequence) == len(sequence):
        # Round completed successfully
        if len(sequence) == 9:
            # All squares used - player wins!
            session['space_memory_game_state'] = 'won'
            session['space_memory_score'] = current_round * 100
            return jsonify({
                'status': 'won',
                'sequence': sequence,
                'round': current_round,
                'score': session['space_memory_score'],
                'game_state': 'won'
            })
        else:
            # Move to next round
            session['space_memory_current_round'] = current_round + 1
            session['space_memory_game_state'] = 'waiting'
            return jsonify({
                'status': 'round_complete',
                'sequence': sequence,
                'round': current_round + 1,
                'game_state': 'waiting'
            })
    
    # Correct input but sequence not complete yet
    return jsonify({
        'status': 'correct',
        'player_sequence': player_sequence,
        'expected_length': len(sequence),
        'game_state': 'playing'
    })

@space_memory_game.route('/api/game-state')
def get_game_state():
    """Get current game state"""
    return jsonify({
        'sequence': session.get('space_memory_sequence', []),
        'player_sequence': session.get('space_memory_player_sequence', []),
        'round': session.get('space_memory_current_round', 1),
        'game_state': session.get('space_memory_game_state', 'waiting'),
        'score': session.get('space_memory_score', 0)
    })