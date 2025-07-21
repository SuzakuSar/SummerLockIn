from flask import Blueprint, render_template, session, request, jsonify
import random

maze_game = Blueprint('maze_game', __name__, template_folder='templates')

# Pre-defined maze layouts (0=path, 1=wall, 2=start, 3=finish)
MAZES = {
    'easy': [
        [2, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    ],
    'medium': [
        [2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    ],
    'hard': [
        [2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    ]
}

def find_start_position(maze):
    """Find the start position (2) in the maze"""
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if cell == 2:
                return row_idx, col_idx
    return 0, 0  # fallback

def find_finish_position(maze):
    """Find the finish position (3) in the maze"""
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if cell == 3:
                return row_idx, col_idx
    return len(maze)-1, len(maze[0])-1  # fallback

def is_valid_move(maze, row, col):
    """Check if a move to the given position is valid"""
    if row < 0 or row >= len(maze):
        return False
    if col < 0 or col >= len(maze[0]):
        return False
    if maze[row][col] == 1:  # wall
        return False
    return True

@maze_game.route('/')
def index():
    """Main maze game page"""
    return render_template('maze_index.html.jinja2')

@maze_game.route('/game/<difficulty>')
def game(difficulty):
    """Start a new maze game with specified difficulty"""
    if difficulty not in MAZES:
        difficulty = 'easy'
    
    # Initialize game state in session
    session['maze_difficulty'] = difficulty
    session['maze_current_maze'] = MAZES[difficulty]
    
    # Find and set starting position
    start_row, start_col = find_start_position(MAZES[difficulty])
    session['maze_player_row'] = start_row
    session['maze_player_col'] = start_col
    session['maze_moves'] = 0
    session['maze_completed'] = False
    
    return render_template('maze_game.html.jinja2', 
                         difficulty=difficulty,
                         maze=MAZES[difficulty],
                         player_row=start_row,
                         player_col=start_col,
                         moves=0,
                         completed=False)

@maze_game.route('/move', methods=['POST'])
def move():
    """Handle player movement"""
    if 'maze_current_maze' not in session:
        return jsonify({'error': 'No active game'})
    
    direction = request.json.get('direction')
    if not direction:
        return jsonify({'error': 'No direction specified'})
    
    # Get current position
    current_row = session.get('maze_player_row', 0)
    current_col = session.get('maze_player_col', 0)
    
    # Calculate new position based on direction
    new_row, new_col = current_row, current_col
    
    if direction == 'up':
        new_row = current_row - 1
    elif direction == 'down':
        new_row = current_row + 1
    elif direction == 'left':
        new_col = current_col - 1
    elif direction == 'right':
        new_col = current_col + 1
    else:
        return jsonify({'error': 'Invalid direction'})
    
    # Check if move is valid
    maze = session['maze_current_maze']
    if not is_valid_move(maze, new_row, new_col):
        return jsonify({
            'success': False,
            'message': 'Invalid move!',
            'player_row': current_row,
            'player_col': current_col,
            'moves': session.get('maze_moves', 0)
        })
    
    # Update position and move count
    session['maze_player_row'] = new_row
    session['maze_player_col'] = new_col
    session['maze_moves'] = session.get('maze_moves', 0) + 1
    
    # Check if player reached the finish
    finish_row, finish_col = find_finish_position(maze)
    completed = (new_row == finish_row and new_col == finish_col)
    session['maze_completed'] = completed
    
    return jsonify({
        'success': True,
        'player_row': new_row,
        'player_col': new_col,
        'moves': session['maze_moves'],
        'completed': completed,
        'message': 'Congratulations! You completed the maze!' if completed else ''
    })

@maze_game.route('/reset')
def reset():
    """Reset the current maze"""
    difficulty = session.get('maze_difficulty', 'easy')
    return game(difficulty)

@maze_game.route('/new_maze')
def new_maze():
    """Generate a random maze from available difficulties"""
    difficulty = random.choice(list(MAZES.keys()))
    return game(difficulty)