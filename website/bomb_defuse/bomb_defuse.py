# File: website/bomb_defuse/bomb_defuse.py
from flask import Blueprint, render_template, request, session, jsonify
import random

bomb_defuse = Blueprint('bomb_defuse', __name__, template_folder='templates')

@bomb_defuse.route('/')
def index():
    """Main bomb defusing game page"""
    # Initialize game state
    session['bomb_defuse_attempts'] = session.get('bomb_defuse_attempts', 0)
    session['bomb_defuse_wins'] = session.get('bomb_defuse_wins', 0)
    session['bomb_defuse_explosions'] = session.get('bomb_defuse_explosions', 0)
    session['bomb_defuse_game_active'] = True
    session['bomb_defuse_time_remaining'] = 30
    
    return render_template('bomb_defuse.html')

@bomb_defuse.route('/cut_wire', methods=['POST'])
def cut_wire():
    """Handle wire cutting attempt"""
    if not session.get('bomb_defuse_game_active', False):
        return jsonify({'error': 'No active game'})
    
    wire_color = request.json.get('wire_color')
    
    # Increment attempts
    session['bomb_defuse_attempts'] = session.get('bomb_defuse_attempts', 0) + 1
    
    # 1% chance to win (defuse bomb)
    success = random.random() < 0.01
    
    if success:
        session['bomb_defuse_wins'] = session.get('bomb_defuse_wins', 0) + 1
        session['bomb_defuse_game_active'] = False
        return jsonify({
            'success': True,
            'message': f'🎉 BOMB DEFUSED! You cut the {wire_color} wire and saved the day!',
            'wire_color': wire_color,
            'stats': get_game_stats()
        })
    else:
        session['bomb_defuse_explosions'] = session.get('bomb_defuse_explosions', 0) + 1
        session['bomb_defuse_game_active'] = False
        return jsonify({
            'success': False,
            'message': f'💥 BOOM! The {wire_color} wire was the wrong choice. Better luck next time!',
            'wire_color': wire_color,
            'stats': get_game_stats()
        })

@bomb_defuse.route('/new_game', methods=['POST'])
def new_game():
    """Start a new bomb defusing game"""
    session['bomb_defuse_game_active'] = True
    session['bomb_defuse_time_remaining'] = 30
    
    return jsonify({
        'message': 'New bomb activated! Choose wisely...',
        'game_active': True
    })

@bomb_defuse.route('/stats')
def get_stats():
    """Get current game statistics"""
    return jsonify(get_game_stats())

def get_game_stats():
    """Helper function to get game statistics"""
    attempts = session.get('bomb_defuse_attempts', 0)
    wins = session.get('bomb_defuse_wins', 0)
    explosions = session.get('bomb_defuse_explosions', 0)
    
    success_rate = (wins / attempts * 100) if attempts > 0 else 0
    
    return {
        'attempts': attempts,
        'wins': wins,
        'explosions': explosions,
        'success_rate': round(success_rate, 2)
    }