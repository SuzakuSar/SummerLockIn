# coin_flip/coin_flip.py
from flask import Blueprint, render_template, request, session, jsonify
import random

coin_flip = Blueprint('coin_flip', __name__, template_folder='templates')

@coin_flip.route('/')
def index():
    """Main coin flip page"""
    # Initialize session data if not exists
    if 'coin_flip_history' not in session:
        session['coin_flip_history'] = []
    if 'coin_flip_stats' not in session:
        session['coin_flip_stats'] = {'heads': 0, 'tails': 0, 'total': 0}
    
    return render_template('coin_flip.html')

@coin_flip.route('/flip', methods=['POST'])
def flip_coin():
    """Handle coin flip via AJAX"""
    # Simple coin flip logic
    result = 'heads' if random.choice([True, False]) else 'tails'
    
    # Update session stats
    if 'coin_flip_stats' not in session:
        session['coin_flip_stats'] = {'heads': 0, 'tails': 0, 'total': 0}
    
    session['coin_flip_stats'][result] += 1
    session['coin_flip_stats']['total'] += 1
    
    # Add to history (keep last 10 flips)
    if 'coin_flip_history' not in session:
        session['coin_flip_history'] = []
    
    session['coin_flip_history'].append(result)
    if len(session['coin_flip_history']) > 10:
        session['coin_flip_history'].pop(0)
    
    # Save session changes
    session.permanent = True
    
    return jsonify({
        'result': result,
        'stats': session['coin_flip_stats'],
        'history': session['coin_flip_history']
    })

@coin_flip.route('/reset', methods=['POST'])
def reset_stats():
    """Reset coin flip statistics"""
    session['coin_flip_history'] = []
    session['coin_flip_stats'] = {'heads': 0, 'tails': 0, 'total': 0}
    session.permanent = True
    
    return jsonify({
        'message': 'Statistics reset successfully',
        'stats': session['coin_flip_stats'],
        'history': session['coin_flip_history']
    })