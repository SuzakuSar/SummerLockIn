"""
Space Invaders Game Blueprint
A simple space invaders clone with basic shooting mechanics
"""

from flask import Blueprint, render_template, session, request, jsonify
import json

# Create blueprint
space_invaders = Blueprint('space_invaders', __name__, template_folder='templates')

@space_invaders.route('/')
def index():
    """Main game page"""
    # Initialize game session data if not exists
    if 'space_invaders_high_score' not in session:
        session['space_invaders_high_score'] = 0
    
    return render_template('space_invaders.html')

@space_invaders.route('/api/score', methods=['POST'])
def save_score():
    """Save game score to session"""
    try:
        data = request.get_json()
        score = data.get('score', 0)
        
        # Validate score is a positive integer
        if not isinstance(score, int) or score < 0:
            return jsonify({'error': 'Invalid score'}), 400
        
        # Update high score if current score is higher
        current_high_score = session.get('space_invaders_high_score', 0)
        if score > current_high_score:
            session['space_invaders_high_score'] = score
            session.permanent = True
            is_high_score = True
        else:
            is_high_score = False
        
        return jsonify({
            'success': True,
            'high_score': session['space_invaders_high_score'],
            'is_high_score': is_high_score
        })
    
    except Exception as e:
        return jsonify({'error': 'Failed to save score'}), 500

@space_invaders.route('/api/high-score')
def get_high_score():
    """Get current high score"""
    high_score = session.get('space_invaders_high_score', 0)
    return jsonify({'high_score': high_score})