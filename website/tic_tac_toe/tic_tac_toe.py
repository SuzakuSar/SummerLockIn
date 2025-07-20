# File: website/tic_tac_toe/tic_tac_toe.py
from flask import Blueprint, render_template, request, jsonify, session
import json

tic_tac_toe = Blueprint('tic_tac_toe', __name__, template_folder='templates')

def init_game():
    """Initialize a new tic tac toe game state"""
    return {
        'board': [['', '', ''], ['', '', ''], ['', '', '']],
        'current_player': 'X',
        'game_over': False,
        'winner': None,
        'moves_count': 0
    }

def check_winner(board):
    """Check if there's a winner on the board"""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    
    return None

def is_board_full(board):
    """Check if the board is full (draw condition)"""
    for row in board:
        for cell in row:
            if cell == '':
                return False
    return True

@tic_tac_toe.route('/')
def index():
    """Main tic tac toe game page"""
    # Initialize game if not exists
    if 'tic_tac_toe_game' not in session:
        session['tic_tac_toe_game'] = init_game()
    
    game_state = session['tic_tac_toe_game']
    return render_template('tic_tac_toe.html.jinja2', game_state=game_state)

@tic_tac_toe.route('/make_move', methods=['POST'])
def make_move():
    """Handle player move via AJAX"""
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    
    # Get current game state
    game_state = session.get('tic_tac_toe_game', init_game())
    
    # Validate move
    if (game_state['game_over'] or 
        row < 0 or row > 2 or col < 0 or col > 2 or 
        game_state['board'][row][col] != ''):
        return jsonify({'success': False, 'message': 'Invalid move'})
    
    # Make the move
    game_state['board'][row][col] = game_state['current_player']
    game_state['moves_count'] += 1
    
    # Check for winner
    winner = check_winner(game_state['board'])
    if winner:
        game_state['winner'] = winner
        game_state['game_over'] = True
    elif is_board_full(game_state['board']):
        game_state['winner'] = 'Draw'
        game_state['game_over'] = True
    else:
        # Switch players
        game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
    
    # Save game state
    session['tic_tac_toe_game'] = game_state
    session.modified = True
    
    return jsonify({
        'success': True,
        'game_state': game_state
    })

@tic_tac_toe.route('/reset_game', methods=['POST'])
def reset_game():
    """Reset the game to initial state"""
    session['tic_tac_toe_game'] = init_game()
    session.modified = True
    
    return jsonify({
        'success': True,
        'game_state': session['tic_tac_toe_game']
    })

@tic_tac_toe.route('/get_game_state')
def get_game_state():
    """Get current game state via AJAX"""
    game_state = session.get('tic_tac_toe_game', init_game())
    return jsonify(game_state)