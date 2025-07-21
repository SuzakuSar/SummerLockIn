# website/connect_dots/connect_dots.py
from flask import Blueprint, render_template, session, jsonify, request
import random
import math

connect_dots = Blueprint('connect_dots', __name__, template_folder='templates')

# Predefined dot patterns for different difficulty levels
DOT_PATTERNS = {
    'easy': [
        {'name': 'Triangle', 'dots': [
            {'x': 50, 'y': 20, 'number': 1},
            {'x': 20, 'y': 70, 'number': 2},
            {'x': 80, 'y': 70, 'number': 3}
        ]},
        {'name': 'Square', 'dots': [
            {'x': 30, 'y': 30, 'number': 1},
            {'x': 70, 'y': 30, 'number': 2},
            {'x': 70, 'y': 70, 'number': 3},
            {'x': 30, 'y': 70, 'number': 4}
        ]}
    ],
    'medium': [
        {'name': 'Pentagon', 'dots': [
            {'x': 50, 'y': 15, 'number': 1},
            {'x': 80, 'y': 35, 'number': 2},
            {'x': 70, 'y': 70, 'number': 3},
            {'x': 30, 'y': 70, 'number': 4},
            {'x': 20, 'y': 35, 'number': 5}
        ]},
        {'name': 'Star', 'dots': [
            {'x': 50, 'y': 10, 'number': 1},
            {'x': 60, 'y': 35, 'number': 2},
            {'x': 85, 'y': 35, 'number': 3},
            {'x': 65, 'y': 55, 'number': 4},
            {'x': 75, 'y': 80, 'number': 5},
            {'x': 50, 'y': 65, 'number': 6},
            {'x': 25, 'y': 80, 'number': 7},
            {'x': 35, 'y': 55, 'number': 8},
            {'x': 15, 'y': 35, 'number': 9},
            {'x': 40, 'y': 35, 'number': 10}
        ]}
    ],
    'hard': [
        {'name': 'House', 'dots': [
            {'x': 20, 'y': 80, 'number': 1},
            {'x': 20, 'y': 50, 'number': 2},
            {'x': 30, 'y': 30, 'number': 3},
            {'x': 50, 'y': 20, 'number': 4},
            {'x': 70, 'y': 30, 'number': 5},
            {'x': 80, 'y': 50, 'number': 6},
            {'x': 80, 'y': 80, 'number': 7},
            {'x': 60, 'y': 80, 'number': 8},
            {'x': 60, 'y': 60, 'number': 9},
            {'x': 40, 'y': 60, 'number': 10},
            {'x': 40, 'y': 80, 'number': 11}
        ]}
    ]
}

@connect_dots.route('/')
def index():
    """Main connect dots game page"""
    # Initialize session variables if not present
    if 'connect_dots_score' not in session:
        session['connect_dots_score'] = 0
    if 'connect_dots_completed' not in session:
        session['connect_dots_completed'] = 0
    
    return render_template('connect_dots_index.html.jinja2')

@connect_dots.route('/game/<difficulty>')
def game(difficulty):
    """Start a new game with specified difficulty"""
    if difficulty not in DOT_PATTERNS:
        difficulty = 'easy'
    
    # Get random pattern for this difficulty
    patterns = DOT_PATTERNS[difficulty]
    current_pattern = random.choice(patterns)
    
    # Store game state in session
    session['connect_dots_current_pattern'] = current_pattern
    session['connect_dots_difficulty'] = difficulty
    session['connect_dots_current_dot'] = 1
    session['connect_dots_game_completed'] = False
    session['connect_dots_connections'] = []
    
    return render_template('connect_dots_game.html.jinja2', 
                         pattern=current_pattern, 
                         difficulty=difficulty)

@connect_dots.route('/api/connect/<int:dot_number>')
def connect_dot(dot_number):
    """Handle dot connection attempt"""
    if 'connect_dots_current_pattern' not in session:
        return jsonify({'error': 'No active game'})
    
    current_dot = session.get('connect_dots_current_dot', 1)
    pattern = session['connect_dots_current_pattern']
    
    # Check if this is the correct next dot
    if dot_number == current_dot:
        # Add connection
        connections = session.get('connect_dots_connections', [])
        
        if current_dot > 1:
            # Find previous and current dot positions
            prev_dot = next(d for d in pattern['dots'] if d['number'] == current_dot - 1)
            curr_dot = next(d for d in pattern['dots'] if d['number'] == current_dot)
            
            connections.append({
                'from': prev_dot,
                'to': curr_dot
            })
        
        session['connect_dots_connections'] = connections
        session['connect_dots_current_dot'] = current_dot + 1
        
        # Check if game is completed
        if current_dot >= len(pattern['dots']):
            session['connect_dots_game_completed'] = True
            session['connect_dots_completed'] = session.get('connect_dots_completed', 0) + 1
            
            # Calculate score based on difficulty
            difficulty_multiplier = {'easy': 10, 'medium': 20, 'hard': 30}
            points = len(pattern['dots']) * difficulty_multiplier[session['connect_dots_difficulty']]
            session['connect_dots_score'] = session.get('connect_dots_score', 0) + points
            
            return jsonify({
                'success': True,
                'completed': True,
                'connections': connections,
                'score': session['connect_dots_score'],
                'points_earned': points
            })
        
        return jsonify({
            'success': True,
            'completed': False,
            'connections': connections,
            'next_dot': session['connect_dots_current_dot']
        })
    else:
        return jsonify({
            'success': False,
            'expected': current_dot,
            'received': dot_number
        })

@connect_dots.route('/api/new-game/<difficulty>')
def new_game(difficulty):
    """Start a new game with fresh pattern"""
    if difficulty not in DOT_PATTERNS:
        difficulty = 'easy'
    
    patterns = DOT_PATTERNS[difficulty]
    current_pattern = random.choice(patterns)
    
    session['connect_dots_current_pattern'] = current_pattern
    session['connect_dots_difficulty'] = difficulty
    session['connect_dots_current_dot'] = 1
    session['connect_dots_game_completed'] = False
    session['connect_dots_connections'] = []
    
    return jsonify({
        'pattern': current_pattern,
        'difficulty': difficulty
    })

@connect_dots.route('/api/stats')
def get_stats():
    """Get current player statistics"""
    return jsonify({
        'score': session.get('connect_dots_score', 0),
        'completed': session.get('connect_dots_completed', 0),
        'current_game': {
            'pattern': session.get('connect_dots_current_pattern'),
            'difficulty': session.get('connect_dots_difficulty'),
            'current_dot': session.get('connect_dots_current_dot', 1),
            'completed': session.get('connect_dots_game_completed', False),
            'connections': session.get('connect_dots_connections', [])
        }
    })