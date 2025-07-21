# File: website/brick_breaker/brick_breaker.py
from flask import Blueprint, render_template, session, request, jsonify

brick_breaker = Blueprint('brick_breaker', __name__, template_folder='templates')

@brick_breaker.route('/')
def index():
    """Main brick breaker game page"""
    # Initialize game stats in session if not exists
    if 'brick_breaker_high_score' not in session:
        session['brick_breaker_high_score'] = 0
    if 'brick_breaker_games_played' not in session:
        session['brick_breaker_games_played'] = 0
    
    return render_template('brick_breaker.html')

@brick_breaker.route('/save_score', methods=['POST'])
def save_score():
    """Save game score to session"""
    try:
        data = request.get_json()
        score = int(data.get('score', 0))
        
        # Update games played
        session['brick_breaker_games_played'] = session.get('brick_breaker_games_played', 0) + 1
        
        # Update high score if needed
        current_high = session.get('brick_breaker_high_score', 0)
        if score > current_high:
            session['brick_breaker_high_score'] = score
            session.permanent = True  # Save session
            return jsonify({
                'success': True, 
                'new_high_score': True,
                'high_score': score
            })
        
        return jsonify({
            'success': True, 
            'new_high_score': False,
            'high_score': current_high
        })
        
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid score'}), 400

@brick_breaker.route('/stats')
def get_stats():
    """Get player statistics"""
    return jsonify({
        'high_score': session.get('brick_breaker_high_score', 0),
        'games_played': session.get('brick_breaker_games_played', 0)
    })