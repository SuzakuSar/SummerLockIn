# Create this folder structure in your website/ directory:


# website/slots_machine/slots_machine.py
from flask import Blueprint, render_template, session, jsonify, request
import random
import time

slots_machine = Blueprint('slots_machine', __name__, template_folder='templates')

# Slot symbols with weighted probabilities (rigged against player)
SYMBOLS = {
    '🍒': {'weight': 25, 'value': 2},    # Most common, lowest payout
    '🍋': {'weight': 20, 'value': 3},
    '🍊': {'weight': 15, 'value': 5},
    '🍇': {'weight': 12, 'value': 8},
    '⭐': {'weight': 8, 'value': 15},
    '💎': {'weight': 5, 'value': 25},
    '👑': {'weight': 3, 'value': 50},
    '💰': {'weight': 2, 'value': 100},   # Rarest, highest payout
}

# Rage-inducing messages
TAUNT_MESSAGES = [
    "So close! Maybe next time? 😏",
    "Ouch! That's gotta hurt! 😈",
    "Better luck never! 💸",
    "Your wallet is getting lighter! 🪶",
    "The house always wins! 🏠",
    "Maybe gambling isn't for you? 🤷‍♀️",
    "Oof! That was painful to watch! 😬",
    "Did you really think you'd win? 🤭",
    "Keep trying, I need a new yacht! ⛵",
    "Your money looks better in my pocket! 💰"
]

NEAR_MISS_MESSAGES = [
    "OH NO! Just one off! 😱",
    "SO CLOSE! Try again! 🎯",
    "Almost had it! Keep spinning! 🔄",
    "Inches away from victory! 📏",
    "Lady Luck is teasing you! 🍀",
    "The slots are mocking you! 🎰"
]

WIN_MESSAGES = [
    "IMPOSSIBLE! You actually won! 🎉",
    "Wait... did that really happen? 😲",
    "Quick! Play again before I fix this! ⚡",
    "Beginner's luck! It won't happen again! 🍀",
    "Enjoy it, it's your last win! 🎊"
]

def init_session():
    """Initialize session variables for slots game"""
    if 'slots_credits' not in session:
        session['slots_credits'] = 100  # Starting credits
    if 'slots_total_spent' not in session:
        session['slots_total_spent'] = 0
    if 'slots_total_spins' not in session:
        session['slots_total_spins'] = 0
    if 'slots_wins' not in session:
        session['slots_wins'] = 0
    if 'slots_losses' not in session:
        session['slots_losses'] = 0

def weighted_choice():
    """Choose a symbol based on weighted probabilities"""
    symbols = list(SYMBOLS.keys())
    weights = [SYMBOLS[symbol]['weight'] for symbol in symbols]
    return random.choices(symbols, weights=weights)[0]

def check_near_miss(reels):
    """Check if this is a near miss (2 out of 3 matching)"""
    if reels[0] == reels[1] and reels[0] != reels[2]:
        return True
    if reels[0] == reels[2] and reels[0] != reels[1]:
        return True
    if reels[1] == reels[2] and reels[1] != reels[0]:
        return True
    return False

def calculate_win(reels, bet_amount):
    """Calculate winnings - heavily rigged against player"""
    # Only pay on exact 3-of-a-kind
    if reels[0] == reels[1] == reels[2]:
        symbol = reels[0]
        base_payout = SYMBOLS[symbol]['value'] * bet_amount
        
        # Add fake "bonus" multiplier that rarely triggers
        if random.random() < 0.01:  # 1% chance
            multiplier = random.choice([2, 3, 5])
            return base_payout * multiplier, f"BONUS x{multiplier}!"
        
        return base_payout, "Winner!"
    
    return 0, ""

@slots_machine.route('/')
def index():
    """Main slots machine page"""
    init_session()
    return render_template('slots_machine.html')

@slots_machine.route('/spin', methods=['POST'])
def spin():
    """Handle slot machine spin"""
    init_session()
    
    data = request.get_json()
    bet_amount = int(data.get('bet', 5))
    
    # Check if player has enough credits
    if session['slots_credits'] < bet_amount:
        return jsonify({
            'error': 'Insufficient credits! Time to add more money! 💸',
            'credits': session['slots_credits']
        })
    
    # Deduct bet
    session['slots_credits'] -= bet_amount
    session['slots_total_spent'] += bet_amount
    session['slots_total_spins'] += 1
    
    # Generate rigged results
    # 95% chance of losing, 4% near miss, 1% win
    rand = random.random()
    
    if rand < 0.01:  # 1% chance to win
        # Generate a winning combination
        winning_symbol = weighted_choice()
        reels = [winning_symbol, winning_symbol, winning_symbol]
        session['slots_wins'] += 1
    elif rand < 0.05:  # 4% chance for near miss
        # Generate a near miss (2 matching)
        symbol = weighted_choice()
        different_symbol = weighted_choice()
        while different_symbol == symbol:
            different_symbol = weighted_choice()
        
        # Randomly place the different symbol
        position = random.randint(0, 2)
        reels = [symbol, symbol, symbol]
        reels[position] = different_symbol
        session['slots_losses'] += 1
    else:  # 95% chance to lose completely
        # Generate completely random (usually losing) combination
        reels = [weighted_choice() for _ in range(3)]
        
        # Make sure it's not accidentally a winner
        while reels[0] == reels[1] == reels[2]:
            reels[2] = weighted_choice()
        
        session['slots_losses'] += 1
    
    # Calculate winnings
    winnings, bonus_text = calculate_win(reels, bet_amount)
    session['slots_credits'] += winnings
    
    # Generate appropriate message
    if winnings > 0:
        message = random.choice(WIN_MESSAGES)
        if bonus_text:
            message = f"{bonus_text} {message}"
    elif check_near_miss(reels):
        message = random.choice(NEAR_MISS_MESSAGES)
    else:
        message = random.choice(TAUNT_MESSAGES)
    
    # Calculate stats for extra rage
    win_rate = (session['slots_wins'] / session['slots_total_spins']) * 100 if session['slots_total_spins'] > 0 else 0
    loss_rate = (session['slots_losses'] / session['slots_total_spins']) * 100 if session['slots_total_spins'] > 0 else 0
    
    return jsonify({
        'reels': reels,
        'winnings': winnings,
        'credits': session['slots_credits'],
        'message': message,
        'stats': {
            'total_spent': session['slots_total_spent'],
            'total_spins': session['slots_total_spins'],
            'wins': session['slots_wins'],
            'losses': session['slots_losses'],
            'win_rate': round(win_rate, 2),
            'loss_rate': round(loss_rate, 2)
        }
    })

@slots_machine.route('/reset')
def reset():
    """Reset game stats (for debugging or rage quitting)"""
    session.pop('slots_credits', None)
    session.pop('slots_total_spent', None)
    session.pop('slots_total_spins', None)
    session.pop('slots_wins', None)
    session.pop('slots_losses', None)
    return jsonify({'message': 'Game reset! Ready to lose again! 😈'})

@slots_machine.route('/add-credits', methods=['POST'])
def add_credits():
    """Add more credits (simulated purchase)"""
    init_session()
    data = request.get_json()
    amount = int(data.get('amount', 50))
    
    session['slots_credits'] += amount
    
    return jsonify({
        'credits': session['slots_credits'],
        'message': f'Added {amount} credits! Time to lose them all! 💸'
    })