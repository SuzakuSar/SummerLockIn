# File: website/block_blast/block_blast.py
from flask import Blueprint, render_template, request, jsonify, session
import random

block_blast = Blueprint('block_blast', __name__, template_folder='templates')

# Game pieces - simple shapes for easy implementation
PIECES = [
    # Single block
    [[1]],
    
    # 2x1 horizontal
    [[1, 1]],
    
    # 2x1 vertical  
    [[1], [1]],
    
    # 3x1 horizontal
    [[1, 1, 1]],
    
    # 3x1 vertical
    [[1], [1], [1]],
    
    # L-shape
    [[1, 0], [1, 1]],
    
    # 2x2 square
    [[1, 1], [1, 1]],
    
    # T-shape
    [[1, 1, 1], [0, 1, 0]]
]

def initialize_game():
    """Initialize a new game session"""
    session['block_blast_grid'] = [[0 for _ in range(10)] for _ in range(10)]
    session['block_blast_score'] = 0
    session['block_blast_current_pieces'] = generate_pieces()
    session.permanent = True

def generate_pieces():
    """Generate 3 random pieces for the player"""
    return [random.choice(PIECES) for _ in range(3)]

def can_place_piece(grid, piece, start_row, start_col):
    """Check if a piece can be placed at the given position"""
    piece_height = len(piece)
    piece_width = len(piece[0])
    
    # Check bounds
    if start_row + piece_height > 10 or start_col + piece_width > 10:
        return False
    
    # Check for collisions
    for r in range(piece_height):
        for c in range(piece_width):
            if piece[r][c] == 1 and grid[start_row + r][start_col + c] != 0:
                return False
    
    return True

def place_piece(grid, piece, start_row, start_col):
    """Place a piece on the grid"""
    piece_height = len(piece)
    piece_width = len(piece[0])
    
    for r in range(piece_height):
        for c in range(piece_width):
            if piece[r][c] == 1:
                grid[start_row + r][start_col + c] = 1

def clear_lines(grid):
    """Clear complete lines and return score"""
    lines_cleared = 0
    
    # Check rows
    for r in range(9, -1, -1):
        if all(grid[r][c] != 0 for c in range(10)):
            for c in range(10):
                grid[r][c] = 0
            lines_cleared += 1
    
    # Check columns
    for c in range(10):
        if all(grid[r][c] != 0 for r in range(10)):
            for r in range(10):
                grid[r][c] = 0
            lines_cleared += 1
    
    return lines_cleared * 100  # 100 points per line

def has_valid_moves(grid, pieces):
    """Check if any piece can be placed on the grid"""
    for piece in pieces:
        if piece is None:  # Already used piece
            continue
        for row in range(10):
            for col in range(10):
                if can_place_piece(grid, piece, row, col):
                    return True
    return False

@block_blast.route('/')
def index():
    """Main game page"""
    if 'block_blast_grid' not in session:
        initialize_game()
    
    return render_template('block_blast.html.jinja2', 
                         grid=session['block_blast_grid'],
                         score=session['block_blast_score'],
                         pieces=session['block_blast_current_pieces'])

@block_blast.route('/place_piece', methods=['POST'])
def place_piece_route():
    """API endpoint to place a piece"""
    data = request.json
    piece_index = data.get('piece_index')
    row = data.get('row')
    col = data.get('col')
    
    if 'block_blast_grid' not in session:
        return jsonify({'success': False, 'message': 'Game not initialized'})
    
    grid = session['block_blast_grid']
    pieces = session['block_blast_current_pieces']
    
    if piece_index < 0 or piece_index >= len(pieces) or pieces[piece_index] is None:
        return jsonify({'success': False, 'message': 'Invalid piece'})
    
    piece = pieces[piece_index]
    
    if not can_place_piece(grid, piece, row, col):
        return jsonify({'success': False, 'message': 'Cannot place piece here'})
    
    # Place the piece
    place_piece(grid, piece, row, col)
    
    # Clear the used piece
    pieces[piece_index] = None
    
    # Clear lines and add score
    lines_score = clear_lines(grid)
    session['block_blast_score'] += lines_score + 10  # 10 base points for placing
    
    # Check if all pieces are used
    if all(piece is None for piece in pieces):
        session['block_blast_current_pieces'] = generate_pieces()
        pieces = session['block_blast_current_pieces']
    
    # Check for game over
    game_over = not has_valid_moves(grid, pieces)
    
    session['block_blast_grid'] = grid
    
    return jsonify({
        'success': True,
        'grid': grid,
        'score': session['block_blast_score'],
        'pieces': pieces,
        'game_over': game_over,
        'lines_cleared': lines_score > 0
    })

@block_blast.route('/new_game', methods=['POST'])
def new_game():
    """Start a new game"""
    initialize_game()
    return jsonify({
        'success': True,
        'grid': session['block_blast_grid'],
        'score': session['block_blast_score'],
        'pieces': session['block_blast_current_pieces']
    })

@block_blast.route('/get_valid_positions', methods=['POST'])
def get_valid_positions():
    """Get valid positions for a piece (for highlighting)"""
    data = request.json
    piece_index = data.get('piece_index')
    
    if 'block_blast_grid' not in session:
        return jsonify({'positions': []})
    
    grid = session['block_blast_grid']
    pieces = session['block_blast_current_pieces']
    
    if piece_index < 0 or piece_index >= len(pieces) or pieces[piece_index] is None:
        return jsonify({'positions': []})
    
    piece = pieces[piece_index]
    valid_positions = []
    
    for row in range(10):
        for col in range(10):
            if can_place_piece(grid, piece, row, col):
                valid_positions.append({'row': row, 'col': col})
    
    return jsonify({'positions': valid_positions})