"""
CLICK CLEAR GAME BLUEPRINT
File Structure to Create:

website/
├── click_clear/
│   ├── __init__.py
│   ├── click_clear.py
│   └── templates/
│       └── click_clear.html

"""

# ==============================================================================
# FILE: website/click_clear/click_clear.py  
# ==============================================================================

from flask import Blueprint, render_template, jsonify, session
import random
import time

# Create blueprint
click_clear = Blueprint('click_clear', __name__, template_folder='templates')

@click_clear.route('/')
def index():
    """Main game page - generates initial objects"""
    
    # Initialize session data
    if 'click_clear_game_active' not in session:
        session['click_clear_game_active'] = False
    
    # Generate random objects for the game
    objects = generate_game_objects()
    
    return render_template('click_clear.html', objects=objects)

@click_clear.route('/new-game')
def new_game():
    """Start a new game - generates fresh objects"""
    
    # Reset game state
    session['click_clear_game_active'] = True
    session['click_clear_start_time'] = time.time()
    session['click_clear_clicks'] = 0
    
    # Generate new objects
    objects = generate_game_objects()
    
    return jsonify({
        'success': True,
        'objects': objects,
        'message': 'New game started!'
    })

@click_clear.route('/object-clicked')
def object_clicked():
    """Handle object click - update session stats"""
    
    if 'click_clear_clicks' not in session:
        session['click_clear_clicks'] = 0
    
    session['click_clear_clicks'] += 1
    
    return jsonify({
        'success': True,
        'clicks': session['click_clear_clicks']
    })

@click_clear.route('/game-complete')
def game_complete():
    """Handle game completion - calculate stats"""
    
    if 'click_clear_start_time' in session:
        completion_time = time.time() - session['click_clear_start_time']
    else:
        completion_time = 0
    
    clicks = session.get('click_clear_clicks', 0)
    
    # Calculate performance rating
    if completion_time < 10 and clicks < 20:
        rating = "⭐⭐⭐ STELLAR PERFORMANCE!"
    elif completion_time < 20 and clicks < 30:
        rating = "⭐⭐ GREAT JOB!"
    elif completion_time < 30:
        rating = "⭐ NICE WORK!"
    else:
        rating = "🌟 MISSION COMPLETE!"
    
    return jsonify({
        'success': True,
        'completion_time': round(completion_time, 1),
        'total_clicks': clicks,
        'rating': rating
    })

def generate_game_objects():
    """Generate random objects for the game"""
    
    # Different object types with their properties
    object_types = [
        {'type': 'asteroid', 'emoji': '☄️', 'size_range': (40, 80), 'points': 10},
        {'type': 'star', 'emoji': '⭐', 'size_range': (30, 60), 'points': 5},
        {'type': 'planet', 'emoji': '🪐', 'size_range': (50, 90), 'points': 15},
        {'type': 'satellite', 'emoji': '🛸', 'size_range': (35, 70), 'points': 12},
        {'type': 'comet', 'emoji': '☄️', 'size_range': (45, 75), 'points': 8},
        {'type': 'moon', 'emoji': '🌙', 'size_range': (40, 65), 'points': 7}
    ]
    
    # Generate 15-25 random objects
    object_count = random.randint(15, 25)
    objects = []
    
    for i in range(object_count):
        obj_type = random.choice(object_types)
        
        # Random position (avoid edges to ensure full visibility)
        x_pos = random.randint(5, 90)  # 5% to 90% of screen width
        y_pos = random.randint(10, 80)  # 10% to 80% of screen height
        
        # Random size within type's range
        size = random.randint(obj_type['size_range'][0], obj_type['size_range'][1])
        
        # Random rotation and animation
        rotation = random.randint(0, 360)
        animation_duration = random.uniform(2.0, 8.0)
        animation_delay = random.uniform(0, 2.0)
        
        objects.append({
            'id': f'obj_{i}',
            'type': obj_type['type'],
            'emoji': obj_type['emoji'],
            'x': x_pos,
            'y': y_pos,
            'size': size,
            'points': obj_type['points'],
            'rotation': rotation,
            'animation_duration': animation_duration,
            'animation_delay': animation_delay,
            'color_hue': random.randint(0, 360)  # For color variations
        })
    
    return objects