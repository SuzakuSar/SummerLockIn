# File: website/coordinate_game/coordinate_game.py
from flask import Blueprint, render_template, request, session, jsonify
import random

coordinate_game = Blueprint('coordinate_game', __name__, template_folder='templates')

@coordinate_game.route('/')
def index():
    """Main coordinate game page"""
    # Initialize game session data if not exists
    if 'coord_score' not in session:
        session['coord_score'] = 0
    if 'coord_attempts' not in session:
        session['coord_attempts'] = 0
    
    # Generate new target coordinates
    generate_new_target()
    
    return render_template('coordinate_game.html.jinja2')

@coordinate_game.route('/guess', methods=['POST'])
def make_guess():
    """Handle coordinate guess submission"""
    try:
        # Get user input
        user_x = int(request.form.get('x_coord', 0))
        user_y = int(request.form.get('y_coord', 0))
        
        # Get target coordinates from session
        target_x = session.get('coord_target_x', 0)
        target_y = session.get('coord_target_y', 0)
        
        # Update attempts
        session['coord_attempts'] = session.get('coord_attempts', 0) + 1
        
        # Check if guess is correct
        is_correct = (user_x == target_x and user_y == target_y)
        
        if is_correct:
            session['coord_score'] = session.get('coord_score', 0) + 1
            message = f"🎯 Correct! The point was at ({target_x}, {target_y})"
            # Generate new target for next round
            generate_new_target()
        else:
            message = f"❌ Wrong! You guessed ({user_x}, {user_y}) but the point was at ({target_x}, {target_y})"
            # Keep same target for retry
        
        return jsonify({
            'correct': is_correct,
            'message': message,
            'score': session['coord_score'],
            'attempts': session['coord_attempts'],
            'accuracy': round((session['coord_score'] / session['coord_attempts']) * 100, 1) if session['coord_attempts'] > 0 else 0,
            'new_target': {
                'x': session.get('coord_target_x', 0),
                'y': session.get('coord_target_y', 0)
            } if is_correct else None
        })
        
    except (ValueError, TypeError):
        return jsonify({
            'correct': False,
            'message': '⚠️ Please enter valid integer coordinates',
            'score': session.get('coord_score', 0),
            'attempts': session.get('coord_attempts', 0),
            'accuracy': 0
        })

@coordinate_game.route('/new-target')
def new_target():
    """Generate new target coordinates"""
    generate_new_target()
    return jsonify({
        'target_x': session['coord_target_x'],
        'target_y': session['coord_target_y']
    })

@coordinate_game.route('/reset')
def reset_game():
    """Reset game statistics"""
    session['coord_score'] = 0
    session['coord_attempts'] = 0
    generate_new_target()
    
    return jsonify({
        'message': 'Game reset!',
        'score': 0,
        'attempts': 0,
        'target_x': session['coord_target_x'],
        'target_y': session['coord_target_y']
    })

def generate_new_target():
    """Generate new random target coordinates"""
    # Generate coordinates in range -10 to 10
    session['coord_target_x'] = random.randint(-10, 10)
    session['coord_target_y'] = random.randint(-10, 10)