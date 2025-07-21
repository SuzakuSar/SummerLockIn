"""
OSU! Clone Game Blueprint
A simple rhythm clicking game where circles appear and must be clicked before they disappear.
"""

from flask import Blueprint, render_template, session, request, jsonify
import random
import time

# Create blueprint with template folder
osu_game = Blueprint('osu_game', __name__, template_folder='templates')

@osu_game.route('/')
def index():
    """Main osu game page"""
    # Initialize game session variables
    if 'osu_score' not in session:
        session['osu_score'] = 0
    if 'osu_high_score' not in session:
        session['osu_high_score'] = 0
    if 'osu_game_active' not in session:
        session['osu_game_active'] = False
    
    return render_template('osu_game.html.jinja2')

@osu_game.route('/start', methods=['POST'])
def start_game():
    """Start a new game"""
    session['osu_score'] = 0
    session['osu_game_active'] = True
    session['osu_game_start_time'] = time.time()
    
    return jsonify({
        'status': 'started',
        'score': session['osu_score']
    })

@osu_game.route('/hit', methods=['POST'])
def hit_circle():
    """Record a successful circle hit"""
    if not session.get('osu_game_active', False):
        return jsonify({'status': 'game_not_active'})
    
    # Increment score
    session['osu_score'] = session.get('osu_score', 0) + 1
    
    return jsonify({
        'status': 'hit',
        'score': session['osu_score']
    })

@osu_game.route('/miss', methods=['POST'])
def miss_circle():
    """Record a missed circle (game over)"""
    session['osu_game_active'] = False
    
    # Update high score if needed
    current_score = session.get('osu_score', 0)
    high_score = session.get('osu_high_score', 0)
    
    if current_score > high_score:
        session['osu_high_score'] = current_score
    
    return jsonify({
        'status': 'game_over',
        'final_score': current_score,
        'high_score': session['osu_high_score']
    })

@osu_game.route('/stats')
def get_stats():
    """Get current game statistics"""
    return jsonify({
        'current_score': session.get('osu_score', 0),
        'high_score': session.get('osu_high_score', 0),
        'game_active': session.get('osu_game_active', False)
    })