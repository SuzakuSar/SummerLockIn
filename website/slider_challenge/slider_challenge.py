# website/slider_challenge/slider_challenge.py
from flask import render_template, request, session, jsonify
import random
from . import slider_challenge

@slider_challenge.route('/')
def index():
    """Main slider challenge page"""
    # Generate a new target if not in session
    if 'sc_target' not in session:
        session['sc_target'] = random.randint(1, 999)  # Random number 1-999
    
    session['sc_attempts'] = session.get('sc_attempts', 0)
    session['sc_best_diff'] = session.get('sc_best_diff', None)
    
    return render_template('slider_challenge.html.jinja2')

@slider_challenge.route('/check', methods=['POST'])
def check_value():
    """Check if the slider value matches the target"""
    data = request.get_json()
    current_value = int(data.get('value', 0))
    target = session.get('sc_target', 500)
    
    # Calculate difference
    difference = abs(current_value - target)
    session['sc_attempts'] = session.get('sc_attempts', 0) + 1
    
    # Update best attempt
    if session.get('sc_best_diff') is None or difference < session.get('sc_best_diff'):
        session['sc_best_diff'] = difference
    
    # Check for exact match
    is_exact = difference == 0
    
    response = {
        'target': target,
        'value': current_value,
        'difference': difference,
        'attempts': session['sc_attempts'],
        'best_diff': session['sc_best_diff'],
        'is_exact': is_exact,
        'message': get_message(difference, is_exact)
    }
    
    return jsonify(response)

@slider_challenge.route('/new-target', methods=['POST'])
def new_target():
    """Generate a new target value"""
    session['sc_target'] = random.randint(1, 999)
    session['sc_attempts'] = 0
    session['sc_best_diff'] = None
    
    return jsonify({
        'target': session['sc_target'],
        'message': 'New target generated! Good luck hitting it exactly...'
    })

def get_message(difference, is_exact):
    """Get appropriate message based on how close they got"""
    if is_exact:
        return "🎉 HOORAY! YOU WASTED YOUR TIME! 🎉"
    elif difference == 1:
        return "SO CLOSE! Off by just 1. The agony!"
    elif difference <= 3:
        return "Close enough to feel the crushing disappointment!"
    elif difference <= 10:
        return "Not even close, but thanks for trying!"
    elif difference <= 25:
        return "Did you even look at the target number?"
    else:
        return "Are you just randomly moving the slider?"