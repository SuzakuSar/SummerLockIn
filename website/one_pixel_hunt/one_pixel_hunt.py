from flask import Blueprint, render_template, session, jsonify, request
import random
import math

# Create blueprint
one_pixel_hunt = Blueprint('one_pixel_hunt', __name__, template_folder='templates')

def generate_pixel_data(level):
    """Generate pixel grid data with one different pixel"""
    # Base grid size starts at 20x20, increases with level
    base_size = 20
    grid_size = min(base_size + (level * 2), 50)  # Cap at 50x50
    
    # Base color (gray scale for simplicity)
    base_color = 128
    
    # Color difference decreases with level (gets harder)
    # Start with 30 difference, decrease to minimum of 3
    max_diff = 30
    min_diff = 3
    color_diff = max(min_diff, max_diff - (level * 2))
    
    # Create the different color
    different_color = base_color + color_diff
    if different_color > 255:
        different_color = base_color - color_diff
    
    # Random position for the different pixel
    target_x = random.randint(0, grid_size - 1)
    target_y = random.randint(0, grid_size - 1)
    
    return {
        'grid_size': grid_size,
        'base_color': base_color,
        'different_color': different_color,
        'target_x': target_x,
        'target_y': target_y,
        'color_diff': color_diff
    }

def init_game_session():
    """Initialize or reset game session data"""
    session['pixel_hunt_level'] = 1
    session['pixel_hunt_score'] = 0
    session['pixel_hunt_attempts'] = 0
    session['pixel_hunt_data'] = generate_pixel_data(1)

@one_pixel_hunt.route('/')
def index():
    """Main game page"""
    # Initialize game if not started
    if 'pixel_hunt_level' not in session:
        init_game_session()
    
    return render_template('pixel_hunt_index.html')

@one_pixel_hunt.route('/api/game-state')
def get_game_state():
    """Get current game state"""
    if 'pixel_hunt_level' not in session:
        init_game_session()
    
    return jsonify({
        'level': session['pixel_hunt_level'],
        'score': session['pixel_hunt_score'],
        'attempts': session['pixel_hunt_attempts'],
        'pixel_data': session['pixel_hunt_data']
    })

@one_pixel_hunt.route('/api/click', methods=['POST'])
def handle_click():
    """Handle pixel click attempt"""
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    
    if 'pixel_hunt_level' not in session:
        init_game_session()
    
    pixel_data = session['pixel_hunt_data']
    session['pixel_hunt_attempts'] += 1
    
    # Check if click is correct
    if x == pixel_data['target_x'] and y == pixel_data['target_y']:
        # Correct! Award points and advance level
        level = session['pixel_hunt_level']
        
        # Scoring: Base 100 points, bonus for difficulty and speed
        base_points = 100
        difficulty_bonus = level * 10
        speed_bonus = max(0, 50 - session['pixel_hunt_attempts'])
        
        points_earned = base_points + difficulty_bonus + speed_bonus
        session['pixel_hunt_score'] += points_earned
        session['pixel_hunt_level'] += 1
        session['pixel_hunt_attempts'] = 0
        
        # Generate new pixel data for next level
        session['pixel_hunt_data'] = generate_pixel_data(session['pixel_hunt_level'])
        
        return jsonify({
            'success': True,
            'message': f'Found it! +{points_earned} points',
            'points_earned': points_earned,
            'new_level': session['pixel_hunt_level'],
            'total_score': session['pixel_hunt_score'],
            'pixel_data': session['pixel_hunt_data']
        })
    else:
        # Wrong pixel
        return jsonify({
            'success': False,
            'message': f'Not quite! Try again. (Attempt {session["pixel_hunt_attempts"]})',
            'attempts': session['pixel_hunt_attempts']
        })

@one_pixel_hunt.route('/api/hint', methods=['POST'])
def get_hint():
    """Provide a hint (reduces score slightly)"""
    if 'pixel_hunt_level' not in session:
        init_game_session()
    
    pixel_data = session['pixel_hunt_data']
    level = session['pixel_hunt_level']
    
    # Deduct small amount of points for hint
    hint_cost = 10
    session['pixel_hunt_score'] = max(0, session['pixel_hunt_score'] - hint_cost)
    
    # Provide hint based on level
    if level <= 3:
        # Early levels: give quadrant hint
        grid_size = pixel_data['grid_size']
        target_x = pixel_data['target_x']
        target_y = pixel_data['target_y']
        
        quad_x = "left" if target_x < grid_size // 2 else "right"
        quad_y = "top" if target_y < grid_size // 2 else "bottom"
        hint_text = f"Look in the {quad_y}-{quad_x} area"
    else:
        # Later levels: give color difference info
        color_diff = pixel_data['color_diff']
        hint_text = f"Color difference: {color_diff} shades"
    
    return jsonify({
        'hint': hint_text,
        'cost': hint_cost,
        'new_score': session['pixel_hunt_score']
    })

@one_pixel_hunt.route('/api/reset', methods=['POST'])
def reset_game():
    """Reset the game"""
    init_game_session()
    
    return jsonify({
        'message': 'Game reset!',
        'pixel_data': session['pixel_hunt_data'],
        'level': 1,
        'score': 0
    })