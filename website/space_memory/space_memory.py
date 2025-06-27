"""
Example: Space Memory Game Blueprint
Shows how to create a new feature following SUMMERLOCKIN conventions
Place this in: website/space_memory/space_memory.py
"""

from flask import Blueprint, render_template, jsonify, request, session
import random
import json

# Create blueprint with template folder
space_memory = Blueprint('space_memory', __name__, template_folder='templates')

# Space-themed symbols for the memory game
SPACE_SYMBOLS = [
    '🌟', '🌙', '🪐', '🛸', '🚀', '☄️', '🌌', '👽', '🛰️', '🔭',
    '⭐', '🌠', '💫', '✨', '🌑', '🌒', '🌓', '🌔', '🌕', '🌖',
    '🌗', '🌘', '🌚', '🌛', '🌜', '🌝', '🌞', '💥', '🔥', '🌎',
    '🌍', '🌏'
]

def generate_game_board(difficulty='easy'):
    """
    Generate a memory game board based on difficulty
    
    Args:
        difficulty: 'easy' (4x4), 'medium' (6x6), 'hard' (8x8)
        
    Returns:
        List of cards with positions and symbols
    """
    # Determine grid size based on difficulty
    sizes = {
        'easy': 4,
        'medium': 6,
        'hard': 8
    }
    
    grid_size = sizes.get(difficulty, 4)
    total_cards = grid_size * grid_size
    pairs_needed = total_cards // 2
    
    # Select symbols for this game
    symbols = SPACE_SYMBOLS[:pairs_needed]
    
    # Create pairs of each symbol
    cards = []
    for symbol in symbols:
        cards.extend([symbol, symbol])  # Add each symbol twice
    
    # Shuffle the cards
    random.shuffle(cards)
    
    # Create board with positions
    board = []
    for i, symbol in enumerate(cards):
        board.append({
            'id': i,
            'symbol': symbol,
            'row': i // grid_size,
            'col': i % grid_size,
            'revealed': False,
            'matched': False
        })
    
    return {
        'board': board,
        'grid_size': grid_size,
        'total_pairs': pairs_needed
    }

@space_memory.route('/')
def index():
    """
    Main page for the space memory game
    """
    # Initialize session if needed
    if 'space_memory_stats' not in session:
        session['space_memory_stats'] = {
            'games_played': 0,
            'games_won': 0,
            'best_time': None,
            'total_moves': 0
        }
    
    return render_template('space_memory.html', stats=session['space_memory_stats'])

@space_memory.route('/api/new-game', methods=['POST'])
def new_game():
    """
    Start a new game with specified difficulty
    """
    data = request.get_json()
    difficulty = data.get('difficulty', 'easy')
    
    # Generate new game board
    game_data = generate_game_board(difficulty)
    
    # Store in session
    session['space_memory_game'] = {
        'board': game_data['board'],
        'grid_size': game_data['grid_size'],
        'total_pairs': game_data['total_pairs'],
        'matched_pairs': 0,
        'moves': 0,
        'start_time': None,
        'difficulty': difficulty
    }
    
    # Return board without symbols (hidden)
    hidden_board = []
    for card in game_data['board']:
        hidden_board.append({
            'id': card['id'],
            'row': card['row'],
            'col': card['col'],
            'revealed': False,
            'matched': False
        })
    
    return jsonify({
        'success': True,
        'board': hidden_board,
        'grid_size': game_data['grid_size']
    })

@space_memory.route('/api/flip-card', methods=['POST'])
def flip_card():
    """
    Handle card flip action
    """
    data = request.get_json()
    card_id = data.get('card_id')
    
    if 'space_memory_game' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    game = session['space_memory_game']
    board = game['board']
    
    # Find the card
    card = next((c for c in board if c['id'] == card_id), None)
    if not card:
        return jsonify({'error': 'Invalid card'}), 400
    
    # Don't flip if already matched
    if card['matched']:
        return jsonify({'error': 'Card already matched'}), 400
    
    # Reveal the card
    card['revealed'] = True
    
    # Get all currently revealed cards (not matched)
    revealed_cards = [c for c in board if c['revealed'] and not c['matched']]
    
    response = {
        'card_id': card_id,
        'symbol': card['symbol'],
        'revealed_count': len(revealed_cards)
    }
    
    # Check for match if two cards are revealed
    if len(revealed_cards) == 2:
        game['moves'] += 1
        card1, card2 = revealed_cards
        
        if card1['symbol'] == card2['symbol']:
            # Match found!
            card1['matched'] = True
            card2['matched'] = True
            game['matched_pairs'] += 1
            
            response['match'] = True
            response['matched_cards'] = [card1['id'], card2['id']]
            
            # Check if game is won
            if game['matched_pairs'] == game['total_pairs']:
                response['game_won'] = True
                response['total_moves'] = game['moves']
                
                # Update stats
                stats = session.get('space_memory_stats', {})
                stats['games_played'] = stats.get('games_played', 0) + 1
                stats['games_won'] = stats.get('games_won', 0) + 1
                stats['total_moves'] = stats.get('total_moves', 0) + game['moves']
                session['space_memory_stats'] = stats
        else:
            # No match
            response['match'] = False
            response['hide_cards'] = [card1['id'], card2['id']]
            
            # Hide cards after delay (handled by frontend)
            for c in revealed_cards:
                c['revealed'] = False
    
    # Save session
    session.modified = True
    
    return jsonify(response)

@space_memory.route('/api/stats')
def get_stats():
    """
    Get player statistics
    """
    stats = session.get('space_memory_stats', {
        'games_played': 0,
        'games_won': 0,
        'best_time': None,
        'total_moves': 0
    })
    
    return jsonify(stats)

@space_memory.route('/api/reset-stats', methods=['POST'])
def reset_stats():
    """
    Reset player statistics
    """
    session['space_memory_stats'] = {
        'games_played': 0,
        'games_won': 0,
        'best_time': None,
        'total_moves': 0
    }
    
    return jsonify({'success': True})