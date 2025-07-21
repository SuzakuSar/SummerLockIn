from flask import Blueprint, render_template, session, request, jsonify
import random

# Create blueprint
balance_scale = Blueprint('balance_scale', __name__, template_folder='templates')

def init_game_session():
    """Initialize or reset the game session data"""
    session['balance_left_weight'] = 0
    session['balance_right_weight'] = 0
    session['balance_moves'] = 0
    session['balance_best_score'] = session.get('balance_best_score', 0)
    session['balance_current_score'] = 0
    session['balance_target'] = random.randint(8, 15)  # Random target weight to reach

def calculate_balance():
    """Calculate the balance state and score"""
    left = session.get('balance_left_weight', 0)
    right = session.get('balance_right_weight', 0)
    
    # Calculate difference (0 = perfect balance)
    difference = abs(left - right)
    
    # Calculate tilt angle (-45 to +45 degrees)
    max_difference = 20  # Max difference before scale tips completely
    if left > right:
        tilt = min(45, (left - right) / max_difference * 45)
    else:
        tilt = max(-45, (right - left) / max_difference * 45)
    
    # Calculate score (higher is better, perfect balance = 100)
    if difference == 0:
        score = 100
    else:
        score = max(0, 100 - (difference * 10))
    
    return {
        'difference': difference,
        'tilt': tilt,
        'score': score,
        'is_balanced': difference <= 1  # Allow small margin for "balanced"
    }

@balance_scale.route('/')
def index():
    """Main game page"""
    # Initialize game if not exists
    if 'balance_left_weight' not in session:
        init_game_session()
    
    # Calculate current balance state
    balance_state = calculate_balance()
    
    game_data = {
        'left_weight': session.get('balance_left_weight', 0),
        'right_weight': session.get('balance_right_weight', 0),
        'moves': session.get('balance_moves', 0),
        'current_score': session.get('balance_current_score', 0),
        'best_score': session.get('balance_best_score', 0),
        'target': session.get('balance_target', 10),
        'balance_state': balance_state
    }
    
    return render_template('balance_scale.html.jinja2', game=game_data)

@balance_scale.route('/add_weight', methods=['POST'])
def add_weight():
    """Add weight to the specified side"""
    data = request.get_json()
    side = data.get('side')  # 'left' or 'right'
    weight = int(data.get('weight', 1))
    
    # Validate input
    if side not in ['left', 'right'] or weight not in [1, 2, 3, 5]:
        return jsonify({'error': 'Invalid input'}), 400
    
    # Initialize session if needed
    if 'balance_left_weight' not in session:
        init_game_session()
    
    # Add weight to the specified side
    if side == 'left':
        session['balance_left_weight'] = session.get('balance_left_weight', 0) + weight
    else:
        session['balance_right_weight'] = session.get('balance_right_weight', 0) + weight
    
    # Increment move counter
    session['balance_moves'] = session.get('balance_moves', 0) + 1
    
    # Calculate new balance state
    balance_state = calculate_balance()
    
    # Update current score
    session['balance_current_score'] = balance_state['score']
    
    # Update best score if this is better
    if balance_state['score'] > session.get('balance_best_score', 0):
        session['balance_best_score'] = balance_state['score']
    
    # Check if target weight reached
    total_weight = session['balance_left_weight'] + session['balance_right_weight']
    target_reached = total_weight >= session.get('balance_target', 10)
    
    return jsonify({
        'left_weight': session['balance_left_weight'],
        'right_weight': session['balance_right_weight'],
        'moves': session['balance_moves'],
        'current_score': session['balance_current_score'],
        'best_score': session['balance_best_score'],
        'balance_state': balance_state,
        'target_reached': target_reached,
        'total_weight': total_weight,
        'target': session.get('balance_target', 10)
    })

@balance_scale.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game to initial state"""
    init_game_session()
    return jsonify({
        'message': 'Game reset successfully',
        'target': session['balance_target']
    })

@balance_scale.route('/new_challenge', methods=['POST'])
def new_challenge():
    """Start a new challenge with a different target"""
    # Keep the best score but reset everything else
    best_score = session.get('balance_best_score', 0)
    init_game_session()
    session['balance_best_score'] = best_score
    
    return jsonify({
        'message': 'New challenge started',
        'target': session['balance_target'],
        'best_score': best_score
    })