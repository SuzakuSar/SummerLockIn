# website/speed_sort/speed_sort.py
from flask import Blueprint, render_template, request, session, jsonify
import random
import time

speed_sort = Blueprint('speed_sort', __name__, template_folder='templates')

# Game data for different types and difficulties
GAME_DATA = {
    'numbers': {
        'easy': lambda: random.sample(range(1, 21), 5),
        'medium': lambda: random.sample(range(1, 51), 8),
        'hard': lambda: random.sample(range(1, 101), 12)
    },
    'colors': {
        'easy': lambda: random.sample(['Red', 'Blue', 'Green', 'Yellow', 'Purple'], 5),
        'medium': lambda: random.sample(['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink', 'Brown'], 6),
        'hard': lambda: random.sample(['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink', 'Brown', 'Black', 'White', 'Gray', 'Cyan'], 8)
    },
    'words': {
        'easy': lambda: random.sample(['Cat', 'Dog', 'Fish', 'Bird', 'Mouse'], 4),
        'medium': lambda: random.sample(['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape'], 6),
        'hard': lambda: random.sample(['Astronomy', 'Biology', 'Chemistry', 'Dentistry', 'Engineering', 'Forensics', 'Geology', 'History'], 7)
    }
}

@speed_sort.route('/')
def index():
    """Main game page"""
    # Initialize session data if not exists
    if 'speed_sort_best_times' not in session:
        session['speed_sort_best_times'] = {}
    
    return render_template('speed_sort_index.html')

@speed_sort.route('/game/<game_type>/<difficulty>')
def game(game_type, difficulty):
    """Start a new game with specified type and difficulty"""
    if game_type not in GAME_DATA or difficulty not in GAME_DATA[game_type]:
        return "Invalid game configuration", 400
    
    # Generate items for this game
    items = GAME_DATA[game_type][difficulty]()
    
    # Store original order and shuffled order in session
    session[f'speed_sort_original_{game_type}_{difficulty}'] = items.copy()
    
    # Shuffle the items
    shuffled_items = items.copy()
    random.shuffle(shuffled_items)
    
    session[f'speed_sort_shuffled_{game_type}_{difficulty}'] = shuffled_items
    session[f'speed_sort_start_time_{game_type}_{difficulty}'] = time.time()
    
    return render_template('speed_sort_game.html', 
                         items=shuffled_items,
                         game_type=game_type,
                         difficulty=difficulty,
                         sort_instruction=get_sort_instruction(game_type))

@speed_sort.route('/api/check-order', methods=['POST'])
def check_order():
    """Check if the submitted order is correct"""
    data = request.get_json()
    game_type = data.get('game_type')
    difficulty = data.get('difficulty')
    submitted_order = data.get('order')
    
    # Get original correct order
    original_key = f'speed_sort_original_{game_type}_{difficulty}'
    start_time_key = f'speed_sort_start_time_{game_type}_{difficulty}'
    
    if original_key not in session or start_time_key not in session:
        return jsonify({'error': 'Game session not found'}), 400
    
    correct_order = session[original_key]
    start_time = session[start_time_key]
    
    # Calculate completion time
    completion_time = round(time.time() - start_time, 2)
    
    # Check if order is correct
    is_correct = False
    if game_type == 'numbers':
        is_correct = submitted_order == sorted(correct_order)
    elif game_type == 'colors':
        # Sort colors alphabetically
        is_correct = submitted_order == sorted(correct_order)
    elif game_type == 'words':
        # Sort words alphabetically
        is_correct = submitted_order == sorted(correct_order)
    
    result = {
        'correct': is_correct,
        'time': completion_time,
        'correct_order': sorted(correct_order) if game_type != 'numbers' else sorted(correct_order)
    }
    
    # Update best time if this was a successful completion
    if is_correct:
        best_times_key = 'speed_sort_best_times'
        game_key = f'{game_type}_{difficulty}'
        
        if best_times_key not in session:
            session[best_times_key] = {}
        
        if game_key not in session[best_times_key] or completion_time < session[best_times_key][game_key]:
            session[best_times_key][game_key] = completion_time
            result['new_record'] = True
        
        session.permanent = True
    
    return jsonify(result)

@speed_sort.route('/api/new-game', methods=['POST'])
def new_game():
    """Generate a new game of the same type and difficulty"""
    data = request.get_json()
    game_type = data.get('game_type')
    difficulty = data.get('difficulty')
    
    if game_type not in GAME_DATA or difficulty not in GAME_DATA[game_type]:
        return jsonify({'error': 'Invalid game configuration'}), 400
    
    # Generate new items
    items = GAME_DATA[game_type][difficulty]()
    session[f'speed_sort_original_{game_type}_{difficulty}'] = items.copy()
    
    # Shuffle the items
    shuffled_items = items.copy()
    random.shuffle(shuffled_items)
    
    session[f'speed_sort_shuffled_{game_type}_{difficulty}'] = shuffled_items
    session[f'speed_sort_start_time_{game_type}_{difficulty}'] = time.time()
    
    return jsonify({
        'items': shuffled_items,
        'sort_instruction': get_sort_instruction(game_type)
    })

@speed_sort.route('/api/leaderboard')
def leaderboard():
    """Get player's best times"""
    best_times = session.get('speed_sort_best_times', {})
    return jsonify(best_times)

def get_sort_instruction(game_type):
    """Get sorting instruction based on game type"""
    instructions = {
        'numbers': 'Sort from smallest to largest',
        'colors': 'Sort alphabetically',
        'words': 'Sort alphabetically'
    }
    return instructions.get(game_type, 'Sort the items')