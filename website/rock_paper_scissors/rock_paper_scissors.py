from flask import Blueprint, render_template, session, jsonify, request
import random

# Create blueprint with template folder
rock_paper_scissors = Blueprint('rock_paper_scissors', __name__, template_folder='templates')

# Game choices and their relationships
CHOICES = ['rock', 'paper', 'scissors']
WINNING_COMBINATIONS = {
    'rock': 'scissors',      # Rock crushes scissors
    'paper': 'rock',         # Paper covers rock
    'scissors': 'paper'      # Scissors cut paper
}

# Choice emojis for visual representation
CHOICE_EMOJIS = {
    'rock': '🪨',
    'paper': '📄', 
    'scissors': '✂️'
}

def initialize_rps_session():
    """Initialize rock paper scissors session data"""
    if 'rps_wins' not in session:
        session['rps_wins'] = 0
    if 'rps_losses' not in session:
        session['rps_losses'] = 0
    if 'rps_ties' not in session:
        session['rps_ties'] = 0
    if 'rps_total_games' not in session:
        session['rps_total_games'] = 0

def determine_winner(player_choice, computer_choice):
    """
    Determine the winner of a rock paper scissors round
    Returns: 'win', 'lose', or 'tie'
    """
    if player_choice == computer_choice:
        return 'tie'
    elif WINNING_COMBINATIONS[player_choice] == computer_choice:
        return 'win'
    else:
        return 'lose'

def get_result_message(result, player_choice, computer_choice):
    """Generate a descriptive result message"""
    messages = {
        'win': {
            ('rock', 'scissors'): "Your rock crushes the computer's scissors!",
            ('paper', 'rock'): "Your paper covers the computer's rock!",
            ('scissors', 'paper'): "Your scissors cut the computer's paper!"
        },
        'lose': {
            ('scissors', 'rock'): "Computer's rock crushes your scissors!",
            ('rock', 'paper'): "Computer's paper covers your rock!",
            ('paper', 'scissors'): "Computer's scissors cut your paper!"
        },
        'tie': "It's a tie! Great minds think alike."
    }
    
    if result == 'tie':
        return messages['tie']
    else:
        return messages[result].get((player_choice, computer_choice), f"You {result}!")

@rock_paper_scissors.route('/')
def index():
    """Main rock paper scissors game page"""
    initialize_rps_session()
    
    # Calculate win percentage
    total_games = session['rps_total_games']
    win_percentage = round((session['rps_wins'] / total_games * 100), 1) if total_games > 0 else 0
    
    return render_template('rock_paper_scissors.html', 
                         wins=session['rps_wins'],
                         losses=session['rps_losses'],
                         ties=session['rps_ties'],
                         total_games=total_games,
                         win_percentage=win_percentage,
                         choices=CHOICES,
                         choice_emojis=CHOICE_EMOJIS)

@rock_paper_scissors.route('/play', methods=['POST'])
def play_round():
    """Play a round of rock paper scissors via AJAX"""
    initialize_rps_session()
    
    # Get player choice from request
    data = request.get_json()
    player_choice = data.get('choice', '').lower()
    
    # Validate player choice
    if player_choice not in CHOICES:
        return jsonify({'error': 'Invalid choice'}), 400
    
    # Generate random computer choice
    computer_choice = random.choice(CHOICES)
    
    # Determine winner
    result = determine_winner(player_choice, computer_choice)
    
    # Update session statistics
    session['rps_total_games'] += 1
    if result == 'win':
        session['rps_wins'] += 1
    elif result == 'lose':
        session['rps_losses'] += 1
    else:
        session['rps_ties'] += 1
    
    # Calculate updated win percentage
    win_percentage = round((session['rps_wins'] / session['rps_total_games'] * 100), 1)
    
    # Get descriptive result message
    result_message = get_result_message(result, player_choice, computer_choice)
    
    return jsonify({
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'result': result,
        'result_message': result_message,
        'player_emoji': CHOICE_EMOJIS[player_choice],
        'computer_emoji': CHOICE_EMOJIS[computer_choice],
        'stats': {
            'wins': session['rps_wins'],
            'losses': session['rps_losses'], 
            'ties': session['rps_ties'],
            'total_games': session['rps_total_games'],
            'win_percentage': win_percentage
        }
    })

@rock_paper_scissors.route('/reset', methods=['POST'])
def reset_stats():
    """Reset game statistics"""
    session['rps_wins'] = 0
    session['rps_losses'] = 0
    session['rps_ties'] = 0
    session['rps_total_games'] = 0
    
    return jsonify({'message': 'Statistics reset successfully'})