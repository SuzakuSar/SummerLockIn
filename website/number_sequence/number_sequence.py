# File: website/number_sequence/number_sequence.py
from flask import Blueprint, render_template, request, session, jsonify
import random
import time

number_sequence = Blueprint('number_sequence', __name__, template_folder='templates')

@number_sequence.route('/')
def index():
    """Main game page"""
    # Initialize session variables if not present
    if 'number_sequence_game_state' not in session:
        session['number_sequence_game_state'] = 'waiting'
        session['number_sequence_current_number'] = 1
        session['number_sequence_score'] = 0
        session['number_sequence_start_time'] = None
        session['number_sequence_numbers'] = []
    
    return render_template('number_sequence.html')

@number_sequence.route('/start-game', methods=['POST'])
def start_game():
    """Start a new game"""
    # Reset game state
    session['number_sequence_game_state'] = 'playing'
    session['number_sequence_current_number'] = 1
    session['number_sequence_score'] = 0
    session['number_sequence_start_time'] = time.time()
    
    # Generate random positions for numbers 1-10
    numbers = []
    for i in range(1, 11):  # Numbers 1 through 10
        numbers.append({
            'number': i,
            'x': random.randint(5, 85),  # Percentage positions
            'y': random.randint(10, 80),
            'clicked': False
        })
    
    session['number_sequence_numbers'] = numbers
    
    return jsonify({
        'status': 'success',
        'numbers': numbers,
        'current_number': session['number_sequence_current_number']
    })

@number_sequence.route('/click-number', methods=['POST'])
def click_number():
    """Handle number click"""
    if session.get('number_sequence_game_state') != 'playing':
        return jsonify({'status': 'error', 'message': 'Game not active'})
    
    clicked_number = request.json.get('number')
    current_number = session.get('number_sequence_current_number', 1)
    
    if clicked_number == current_number:
        # Correct number clicked
        session['number_sequence_current_number'] = current_number + 1
        session['number_sequence_score'] += 10
        
        # Mark number as clicked
        numbers = session.get('number_sequence_numbers', [])
        for num in numbers:
            if num['number'] == clicked_number:
                num['clicked'] = True
                break
        session['number_sequence_numbers'] = numbers
        
        # Check if game is complete
        if current_number >= 10:
            # Game complete
            end_time = time.time()
            start_time = session.get('number_sequence_start_time', end_time)
            total_time = round(end_time - start_time, 2)
            
            session['number_sequence_game_state'] = 'completed'
            
            return jsonify({
                'status': 'complete',
                'score': session['number_sequence_score'],
                'time': total_time,
                'message': f'Congratulations! Completed in {total_time}s'
            })
        
        return jsonify({
            'status': 'correct',
            'next_number': session['number_sequence_current_number'],
            'score': session['number_sequence_score']
        })
    
    else:
        # Wrong number clicked
        session['number_sequence_game_state'] = 'failed'
        return jsonify({
            'status': 'wrong',
            'message': f'Wrong! You clicked {clicked_number}, needed {current_number}',
            'score': session['number_sequence_score']
        })

@number_sequence.route('/reset-game', methods=['POST'])
def reset_game():
    """Reset the game"""
    session['number_sequence_game_state'] = 'waiting'
    session['number_sequence_current_number'] = 1
    session['number_sequence_score'] = 0
    session['number_sequence_start_time'] = None
    session['number_sequence_numbers'] = []
    
    return jsonify({'status': 'reset'})

@number_sequence.route('/get-game-state')
def get_game_state():
    """Get current game state"""
    return jsonify({
        'game_state': session.get('number_sequence_game_state', 'waiting'),
        'current_number': session.get('number_sequence_current_number', 1),
        'score': session.get('number_sequence_score', 0),
        'numbers': session.get('number_sequence_numbers', [])
    })