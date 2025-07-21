from flask import Blueprint, render_template, request, session, jsonify
import random
import time

# Create blueprint with template folder
lockpick_game = Blueprint('lockpick_game', __name__, template_folder='templates')

def generate_lock_data():
    """Generate random lock configuration with sweet spots for each pin"""
    num_pins = random.randint(3, 5)  # 3-5 pins for variety
    pins = []
    
    for i in range(num_pins):
        # Sweet spot is a range of positions (0-100)
        sweet_spot_center = random.randint(15, 85)
        sweet_spot_size = random.randint(8, 15)  # Size of sweet spot
        
        pins.append({
            'id': i,
            'sweet_spot_min': max(0, sweet_spot_center - sweet_spot_size // 2),
            'sweet_spot_max': min(100, sweet_spot_center + sweet_spot_size // 2),
            'is_set': False
        })
    
    return {
        'pins': pins,
        'current_pin': 0,
        'picks_remaining': 3,  # Player gets 3 picks before failure
        'start_time': time.time(),
        'difficulty': 'normal'
    }

@lockpick_game.route('/')
def index():
    """Main lockpicking game page"""
    return render_template('lockpick_game.html')

@lockpick_game.route('/start_game', methods=['POST'])
def start_game():
    """Initialize a new lockpicking game"""
    difficulty = request.json.get('difficulty', 'normal')
    
    # Generate lock data based on difficulty
    lock_data = generate_lock_data()
    
    if difficulty == 'easy':
        lock_data['picks_remaining'] = 5
        # Make sweet spots slightly larger for easy mode
        for pin in lock_data['pins']:
            current_size = pin['sweet_spot_max'] - pin['sweet_spot_min']
            increase = current_size * 0.3
            pin['sweet_spot_min'] = max(0, pin['sweet_spot_min'] - increase // 2)
            pin['sweet_spot_max'] = min(100, pin['sweet_spot_max'] + increase // 2)
    elif difficulty == 'hard':
        lock_data['picks_remaining'] = 2
        # Make sweet spots smaller for hard mode
        for pin in lock_data['pins']:
            current_size = pin['sweet_spot_max'] - pin['sweet_spot_min']
            decrease = current_size * 0.3
            center = (pin['sweet_spot_min'] + pin['sweet_spot_max']) / 2
            pin['sweet_spot_min'] = center - (current_size - decrease) // 2
            pin['sweet_spot_max'] = center + (current_size - decrease) // 2
    
    lock_data['difficulty'] = difficulty
    
    # Store in session with feature prefix
    session['lockpick_game_data'] = lock_data
    
    return jsonify({
        'success': True,
        'num_pins': len(lock_data['pins']),
        'picks_remaining': lock_data['picks_remaining'],
        'current_pin': lock_data['current_pin'],
        'difficulty': difficulty
    })

@lockpick_game.route('/check_position', methods=['POST'])
def check_position():
    """Check if current pick position is in sweet spot"""
    if 'lockpick_game_data' not in session:
        return jsonify({'error': 'No active game'})
    
    position = request.json.get('position', 0)  # 0-100 position
    pressure = request.json.get('pressure', 0)  # 0-100 pressure
    
    lock_data = session['lockpick_game_data']
    current_pin_idx = lock_data['current_pin']
    
    if current_pin_idx >= len(lock_data['pins']):
        return jsonify({'error': 'Game already completed'})
    
    current_pin = lock_data['pins'][current_pin_idx]
    
    # Check if position is in sweet spot
    in_sweet_spot = (current_pin['sweet_spot_min'] <= position <= current_pin['sweet_spot_max'])
    
    # Calculate feedback based on distance from sweet spot
    if in_sweet_spot:
        distance = 0
        feedback = 'perfect'
    else:
        # Calculate distance to nearest edge of sweet spot
        if position < current_pin['sweet_spot_min']:
            distance = current_pin['sweet_spot_min'] - position
        else:
            distance = position - current_pin['sweet_spot_max']
        
        # Provide graduated feedback
        if distance <= 5:
            feedback = 'very_close'
        elif distance <= 15:
            feedback = 'close'
        elif distance <= 30:
            feedback = 'warm'
        else:
            feedback = 'cold'
    
    return jsonify({
        'feedback': feedback,
        'in_sweet_spot': in_sweet_spot,
        'distance': distance,
        'position': position
    })

@lockpick_game.route('/apply_pressure', methods=['POST'])
def apply_pressure():
    """Apply pressure to try to set the current pin"""
    if 'lockpick_game_data' not in session:
        return jsonify({'error': 'No active game'})
    
    position = request.json.get('position', 0)
    pressure = request.json.get('pressure', 100)
    
    lock_data = session['lockpick_game_data']
    current_pin_idx = lock_data['current_pin']
    
    if current_pin_idx >= len(lock_data['pins']):
        return jsonify({'error': 'Game already completed'})
    
    current_pin = lock_data['pins'][current_pin_idx]
    
    # Check if position is in sweet spot
    in_sweet_spot = (current_pin['sweet_spot_min'] <= position <= current_pin['sweet_spot_max'])
    
    if in_sweet_spot and pressure >= 80:
        # Pin successfully set!
        current_pin['is_set'] = True
        lock_data['current_pin'] += 1
        
        # Check if all pins are set (game won)
        all_set = all(pin['is_set'] for pin in lock_data['pins'])
        
        if all_set:
            # Game completed successfully
            completion_time = time.time() - lock_data['start_time']
            
            # Calculate score based on time and difficulty
            base_score = 1000
            time_penalty = min(500, completion_time * 10)
            difficulty_bonus = {'easy': 0, 'normal': 200, 'hard': 500}[lock_data['difficulty']]
            picks_bonus = lock_data['picks_remaining'] * 50
            
            final_score = int(base_score - time_penalty + difficulty_bonus + picks_bonus)
            
            session['lockpick_game_data'] = lock_data
            
            return jsonify({
                'success': True,
                'pin_set': True,
                'game_won': True,
                'completion_time': round(completion_time, 2),
                'final_score': final_score,
                'pins_remaining': 0
            })
        else:
            session['lockpick_game_data'] = lock_data
            return jsonify({
                'success': True,
                'pin_set': True,
                'game_won': False,
                'current_pin': lock_data['current_pin'],
                'pins_remaining': len(lock_data['pins']) - lock_data['current_pin']
            })
    
    else:
        # Pick broke or wrong position
        lock_data['picks_remaining'] -= 1
        
        if lock_data['picks_remaining'] <= 0:
            # Game over
            session['lockpick_game_data'] = lock_data
            return jsonify({
                'success': False,
                'pick_broke': True,
                'game_over': True,
                'picks_remaining': 0
            })
        else:
            session['lockpick_game_data'] = lock_data
            return jsonify({
                'success': False,
                'pick_broke': True,
                'game_over': False,
                'picks_remaining': lock_data['picks_remaining']
            })

@lockpick_game.route('/get_game_state', methods=['GET'])
def get_game_state():
    """Get current game state"""
    if 'lockpick_game_data' not in session:
        return jsonify({'error': 'No active game'})
    
    lock_data = session['lockpick_game_data']
    
    return jsonify({
        'current_pin': lock_data['current_pin'],
        'total_pins': len(lock_data['pins']),
        'picks_remaining': lock_data['picks_remaining'],
        'difficulty': lock_data['difficulty'],
        'pins_status': [pin['is_set'] for pin in lock_data['pins']]
    })

@lockpick_game.route('/reset_game', methods=['POST'])
def reset_game():
    """Reset/clear current game"""
    if 'lockpick_game_data' in session:
        del session['lockpick_game_data']
    
    return jsonify({'success': True, 'message': 'Game reset'})