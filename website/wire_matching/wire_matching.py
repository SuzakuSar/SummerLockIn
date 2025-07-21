from flask import Blueprint, render_template, request, session, jsonify
import random

wire_matching = Blueprint('wire_matching', __name__, template_folder='templates')

# Available wire colors
WIRE_COLORS = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

def generate_wire_puzzle():
    """Generate a new wire matching puzzle"""
    # Select 4-6 random colors for the puzzle
    num_wires = random.randint(4, 6)
    selected_colors = random.sample(WIRE_COLORS, num_wires)
    
    # Create left and right wire lists (same colors, different order)
    left_wires = selected_colors.copy()
    right_wires = selected_colors.copy()
    random.shuffle(right_wires)
    
    return {
        'left_wires': left_wires,
        'right_wires': right_wires,
        'total_wires': num_wires
    }

@wire_matching.route('/')
def index():
    """Main wire matching game page"""
    # Initialize session variables if not present
    if 'wire_matching_games_won' not in session:
        session['wire_matching_games_won'] = 0
    if 'wire_matching_games_played' not in session:
        session['wire_matching_games_played'] = 0
    
    # Generate new puzzle
    puzzle = generate_wire_puzzle()
    session['wire_matching_current_puzzle'] = puzzle
    session['wire_matching_connections'] = []
    session['wire_matching_game_complete'] = False
    
    return render_template('wire_matching.html.jinja2', 
                         puzzle=puzzle,
                         games_won=session['wire_matching_games_won'],
                         games_played=session['wire_matching_games_played'])

@wire_matching.route('/connect', methods=['POST'])
def connect_wires():
    """Handle wire connection attempts"""
    data = request.get_json()
    left_index = data.get('left_index')
    right_index = data.get('right_index')
    
    puzzle = session.get('wire_matching_current_puzzle')
    connections = session.get('wire_matching_connections', [])
    
    if not puzzle:
        return jsonify({'success': False, 'message': 'No active game'})
    
    # Check if this left wire is already connected
    for conn in connections:
        if conn['left_index'] == left_index:
            return jsonify({'success': False, 'message': 'Wire already connected'})
    
    # Get the colors
    left_color = puzzle['left_wires'][left_index]
    right_color = puzzle['right_wires'][right_index]
    
    # Check if colors match
    if left_color == right_color:
        # Successful connection
        connection = {
            'left_index': left_index,
            'right_index': right_index,
            'color': left_color,
            'correct': True
        }
        connections.append(connection)
        session['wire_matching_connections'] = connections
        
        # Check if game is complete
        if len(connections) == puzzle['total_wires']:
            session['wire_matching_game_complete'] = True
            session['wire_matching_games_won'] += 1
            session['wire_matching_games_played'] += 1
            
            return jsonify({
                'success': True, 
                'correct': True,
                'game_complete': True,
                'message': 'All wires connected! Task complete!',
                'connection': connection
            })
        
        return jsonify({
            'success': True, 
            'correct': True,
            'game_complete': False,
            'message': 'Wire connected successfully!',
            'connection': connection
        })
    else:
        # Wrong connection - game over
        session['wire_matching_games_played'] += 1
        return jsonify({
            'success': True, 
            'correct': False,
            'game_over': True,
            'message': f'Wrong connection! {left_color} ≠ {right_color}',
            'correct_color': left_color
        })

@wire_matching.route('/new-game', methods=['POST'])
def new_game():
    """Start a new wire matching game"""
    puzzle = generate_wire_puzzle()
    session['wire_matching_current_puzzle'] = puzzle
    session['wire_matching_connections'] = []
    session['wire_matching_game_complete'] = False
    
    return jsonify({
        'success': True,
        'puzzle': puzzle
    })
