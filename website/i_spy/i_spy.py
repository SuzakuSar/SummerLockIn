# website/i_spy/i_spy.py
from flask import Blueprint, render_template, session, request, jsonify
import random

i_spy = Blueprint('i_spy', __name__, template_folder='templates')

# Simple objects to find with their positions (x, y as percentages)
GAME_OBJECTS = [
    {"name": "Red Ball", "x": 15, "y": 25, "size": 30, "color": "#ff4444"},
    {"name": "Blue Star", "x": 65, "y": 40, "size": 25, "color": "#4444ff"},
    {"name": "Green Apple", "x": 35, "y": 60, "size": 35, "color": "#44ff44"},
    {"name": "Yellow Sun", "x": 80, "y": 20, "size": 40, "color": "#ffff44"},
    {"name": "Purple Heart", "x": 50, "y": 80, "size": 28, "color": "#ff44ff"},
]

@i_spy.route('/')
def index():
    """Main I Spy game page"""
    # Initialize session data
    if 'i_spy_found_objects' not in session:
        session['i_spy_found_objects'] = []
        session['i_spy_total_objects'] = len(GAME_OBJECTS)
        session['i_spy_score'] = 0
    
    # Get current game state
    found_objects = session.get('i_spy_found_objects', [])
    total_objects = session.get('i_spy_total_objects', len(GAME_OBJECTS))
    score = session.get('i_spy_score', 0)
    
    # Check if game is complete
    game_complete = len(found_objects) == total_objects
    
    # Create objects list with found status
    objects_with_status = []
    for i, obj in enumerate(GAME_OBJECTS):
        objects_with_status.append({
            **obj,
            'id': i,
            'found': i in found_objects
        })
    
    return render_template('i_spy.html.jinja2', 
                         objects=objects_with_status,
                         found_count=len(found_objects),
                         total_count=total_objects,
                         score=score,
                         game_complete=game_complete)

@i_spy.route('/click', methods=['POST'])
def handle_click():
    """Handle clicking on the game area"""
    data = request.get_json()
    click_x = float(data.get('x', 0))
    click_y = float(data.get('y', 0))
    
    # Initialize session if needed
    if 'i_spy_found_objects' not in session:
        session['i_spy_found_objects'] = []
        session['i_spy_score'] = 0
    
    found_objects = session['i_spy_found_objects']
    
    # Check if click is near any unfound object
    for i, obj in enumerate(GAME_OBJECTS):
        if i not in found_objects:
            # Check if click is within object area (with some tolerance)
            tolerance = max(obj['size'] / 2, 20)  # At least 20px tolerance
            
            distance_x = abs(click_x - obj['x'])
            distance_y = abs(click_y - obj['y'])
            
            if distance_x <= tolerance / 100 * 100 and distance_y <= tolerance / 100 * 100:
                # Found object!
                found_objects.append(i)
                session['i_spy_found_objects'] = found_objects
                session['i_spy_score'] = session.get('i_spy_score', 0) + 10
                
                return jsonify({
                    'success': True,
                    'found_object': obj['name'],
                    'object_id': i,
                    'score': session['i_spy_score'],
                    'total_found': len(found_objects),
                    'game_complete': len(found_objects) == len(GAME_OBJECTS)
                })
    
    # No object found at click location
    return jsonify({
        'success': False,
        'message': 'Nothing here! Keep looking...'
    })

@i_spy.route('/reset')
def reset_game():
    """Reset the game"""
    session.pop('i_spy_found_objects', None)
    session.pop('i_spy_score', None)
    session.pop('i_spy_total_objects', None)
    return jsonify({'success': True})

@i_spy.route('/hint')
def get_hint():
    """Get a hint for the next object to find"""
    found_objects = session.get('i_spy_found_objects', [])
    
    # Find first unfound object
    for i, obj in enumerate(GAME_OBJECTS):
        if i not in found_objects:
            return jsonify({
                'hint': f"Look for a {obj['name'].lower()} in the {get_area_hint(obj['x'], obj['y'])} area",
                'object_name': obj['name']
            })
    
    return jsonify({'hint': 'All objects found! Great job!'})

def get_area_hint(x, y):
    """Convert coordinates to area description"""
    h_area = "left" if x < 33 else "center" if x < 66 else "right"
    v_area = "top" if y < 33 else "middle" if y < 66 else "bottom"
    
    if h_area == "center" and v_area == "middle":
        return "center"
    elif h_area == "center":
        return v_area
    elif v_area == "middle":
        return h_area
    else:
        return f"{v_area}-{h_area}"