# pong/pong.py
# Simple Pong game implementation

from flask import Blueprint, render_template, session, request, jsonify
import random

# Create blueprint
pong = Blueprint('pong', __name__, template_folder='templates')

@pong.route('/')
def index():
    """Main Pong game page"""
    # Initialize game session data if not exists
    if 'pong_high_score' not in session:
        session['pong_high_score'] = 0
    if 'pong_games_played' not in session:
        session['pong_games_played'] = 0
    
    return render_template('pong.html')

@pong.route('/api/score', methods=['POST'])
def update_score():
    """Update high score and games played"""
    try:
        data = request.get_json()
        score = int(data.get('score', 0))
        
        # Update games played
        session['pong_games_played'] = session.get('pong_games_played', 0) + 1
        
        # Update high score if needed
        current_high = session.get('pong_high_score', 0)
        if score > current_high:
            session['pong_high_score'] = score
            is_new_high = True
        else:
            is_new_high = False
        
        return jsonify({
            'success': True,
            'high_score': session['pong_high_score'],
            'games_played': session['pong_games_played'],
            'is_new_high': is_new_high
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@pong.route('/api/stats')
def get_stats():
    """Get current game statistics"""
    return jsonify({
        'high_score': session.get('pong_high_score', 0),
        'games_played': session.get('pong_games_played', 0)
    })