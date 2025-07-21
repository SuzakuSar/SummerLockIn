# File: website/game_2048/game_2048.py
from flask import Blueprint, render_template, request, session, jsonify
import random
import json

game_2048 = Blueprint('game_2048', __name__, template_folder='templates')

def initialize_game():
    """Initialize a new 2048 game board"""
    board = [[0 for _ in range(4)] for _ in range(4)]
    score = 0
    add_random_tile(board)
    add_random_tile(board)
    return board, score

def add_random_tile(board):
    """Add a random tile (2 or 4) to an empty position"""
    empty_cells = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 2 if random.random() < 0.9 else 4

def move_left(board):
    """Move and merge tiles to the left"""
    new_board = [row[:] for row in board]
    score_gained = 0
    moved = False
    
    for i in range(4):
        # Remove zeros
        row = [cell for cell in new_board[i] if cell != 0]
        
        # Merge adjacent same values
        merged_row = []
        j = 0
        while j < len(row):
            if j < len(row) - 1 and row[j] == row[j + 1]:
                merged_value = row[j] * 2
                merged_row.append(merged_value)
                score_gained += merged_value
                j += 2
            else:
                merged_row.append(row[j])
                j += 1
        
        # Pad with zeros
        merged_row.extend([0] * (4 - len(merged_row)))
        
        # Check if anything moved
        if new_board[i] != merged_row:
            moved = True
        
        new_board[i] = merged_row
    
    return new_board, score_gained, moved

def move_right(board):
    """Move and merge tiles to the right"""
    # Reverse, move left, reverse back
    reversed_board = [row[::-1] for row in board]
    moved_board, score_gained, moved = move_left(reversed_board)
    final_board = [row[::-1] for row in moved_board]
    return final_board, score_gained, moved

def move_up(board):
    """Move and merge tiles up"""
    # Transpose, move left, transpose back
    transposed = [[board[j][i] for j in range(4)] for i in range(4)]
    moved_board, score_gained, moved = move_left(transposed)
    final_board = [[moved_board[j][i] for j in range(4)] for i in range(4)]
    return final_board, score_gained, moved

def move_down(board):
    """Move and merge tiles down"""
    # Transpose, move right, transpose back
    transposed = [[board[j][i] for j in range(4)] for i in range(4)]
    moved_board, score_gained, moved = move_right(transposed)
    final_board = [[moved_board[j][i] for j in range(4)] for i in range(4)]
    return final_board, score_gained, moved

def is_game_over(board):
    """Check if game is over (no moves possible)"""
    # Check for empty cells
    for row in board:
        if 0 in row:
            return False
    
    # Check for possible merges
    for i in range(4):
        for j in range(4):
            current = board[i][j]
            # Check right neighbor
            if j < 3 and board[i][j + 1] == current:
                return False
            # Check bottom neighbor
            if i < 3 and board[i + 1][j] == current:
                return False
    
    return True

def has_won(board):
    """Check if player has reached 2048"""
    for row in board:
        if 2048 in row:
            return True
    return False

def get_max_tile(board):
    """Get the highest tile value on the board"""
    max_val = 0
    for row in board:
        max_val = max(max_val, max(row))
    return max_val

@game_2048.route('/')
def index():
    """Main game page"""
    # Initialize game if not exists
    if 'game_2048_board' not in session:
        board, score = initialize_game()
        session['game_2048_board'] = board
        session['game_2048_score'] = score
        session['game_2048_best_score'] = 0
        session['game_2048_moves'] = 0
    
    board = session['game_2048_board']
    score = session['game_2048_score']
    best_score = session.get('game_2048_best_score', 0)
    moves = session.get('game_2048_moves', 0)
    max_tile = get_max_tile(board)
    
    game_over = is_game_over(board)
    won = has_won(board)
    
    return render_template('game_2048.html.jinja2', 
                         board=board, 
                         score=score, 
                         best_score=best_score,
                         moves=moves,
                         max_tile=max_tile,
                         game_over=game_over,
                         won=won)

@game_2048.route('/move', methods=['POST'])
def make_move():
    """Handle move requests"""
    data = request.get_json()
    direction = data.get('direction')
    
    if 'game_2048_board' not in session:
        return jsonify({'error': 'No game in progress'}), 400
    
    board = session['game_2048_board']
    current_score = session['game_2048_score']
    
    # Apply move based on direction
    if direction == 'left':
        new_board, score_gained, moved = move_left(board)
    elif direction == 'right':
        new_board, score_gained, moved = move_right(board)
    elif direction == 'up':
        new_board, score_gained, moved = move_up(board)
    elif direction == 'down':
        new_board, score_gained, moved = move_down(board)
    else:
        return jsonify({'error': 'Invalid direction'}), 400
    
    if not moved:
        return jsonify({'moved': False, 'board': board, 'score': current_score})
    
    # Add random tile after successful move
    add_random_tile(new_board)
    
    # Update session
    new_score = current_score + score_gained
    session['game_2048_board'] = new_board
    session['game_2048_score'] = new_score
    session['game_2048_moves'] = session.get('game_2048_moves', 0) + 1
    
    # Update best score
    best_score = session.get('game_2048_best_score', 0)
    if new_score > best_score:
        session['game_2048_best_score'] = new_score
        best_score = new_score
    
    # Check game state
    game_over = is_game_over(new_board)
    won = has_won(new_board)
    max_tile = get_max_tile(new_board)
    
    return jsonify({
        'moved': True,
        'board': new_board,
        'score': new_score,
        'best_score': best_score,
        'moves': session['game_2048_moves'],
        'max_tile': max_tile,
        'game_over': game_over,
        'won': won,
        'score_gained': score_gained
    })

@game_2048.route('/new-game', methods=['POST'])
def new_game():
    """Start a new game"""
    board, score = initialize_game()
    
    # Update best score before resetting
    current_score = session.get('game_2048_score', 0)
    best_score = session.get('game_2048_best_score', 0)
    if current_score > best_score:
        session['game_2048_best_score'] = current_score
        best_score = current_score
    
    session['game_2048_board'] = board
    session['game_2048_score'] = score
    session['game_2048_moves'] = 0
    
    return jsonify({
        'board': board,
        'score': score,
        'best_score': best_score,
        'moves': 0,
        'max_tile': get_max_tile(board),
        'game_over': False,
        'won': False
    })

@game_2048.route('/api/stats')
def get_stats():
    """Get current game statistics"""
    board = session.get('game_2048_board', [[0]*4 for _ in range(4)])
    return jsonify({
        'score': session.get('game_2048_score', 0),
        'best_score': session.get('game_2048_best_score', 0),
        'moves': session.get('game_2048_moves', 0),
        'max_tile': get_max_tile(board),
        'game_over': is_game_over(board),
        'won': has_won(board)
    })