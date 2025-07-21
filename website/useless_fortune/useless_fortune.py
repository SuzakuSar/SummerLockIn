from flask import Blueprint, render_template, session, jsonify
import random

# Create blueprint
useless_fortune = Blueprint('useless_fortune', __name__, template_folder='templates')

# Collection of genuinely useless or hindering fortunes
USELESS_FORTUNES = [
    {
        "card": "The Procrastination Mystique",
        "fortune": "You will find the perfect time to start that project... tomorrow. And the next day. And the day after that.",
        "symbol": "⏰",
        "color": "#ff6b6b"
    },
    {
        "card": "The Misplaced Keys Oracle",
        "fortune": "Your keys will relocate themselves to increasingly creative hiding spots just when you're already running late.",
        "symbol": "🗝️",
        "color": "#4ecdc4"
    },
    {
        "card": "The WiFi Disconnect Prophecy",
        "fortune": "Your internet connection will mysteriously fail only during important video calls and never during cat video binges.",
        "symbol": "📶",
        "color": "#45b7d1"
    },
    {
        "card": "The Sock Vanishing Enigma",
        "fortune": "Single socks will continue their migration to an alternate dimension, leaving you with a drawer full of lonely companions.",
        "symbol": "🧦",
        "color": "#f9ca24"
    },
    {
        "card": "The Traffic Light Conspiracy",
        "fortune": "Every traffic light will turn red the moment you approach, as if they're personally invested in your tardiness.",
        "symbol": "🚦",
        "color": "#f0932b"
    },
    {
        "card": "The Phone Battery Betrayal",
        "fortune": "Your phone battery will reach critically low levels only when you need GPS directions in unfamiliar territory.",
        "symbol": "🔋",
        "color": "#eb4d4b"
    },
    {
        "card": "The Autocorrect Sabotage",
        "fortune": "Your autocorrect will develop increasingly creative interpretations of what you meant to say in professional emails.",
        "symbol": "📱",
        "color": "#6c5ce7"
    },
    {
        "card": "The Elevator Button Rebellion",
        "fortune": "Elevator buttons will require exactly three presses to work, but only you will know this cosmic truth.",
        "symbol": "🛗",
        "color": "#a29bfe"
    },
    {
        "card": "The Snooze Button Temptation",
        "fortune": "Your alarm's snooze button will develop magnetic properties that irresistibly attract your sleepy finger.",
        "symbol": "⏰",
        "color": "#fd79a8"
    },
    {
        "card": "The Headphone Tangle Mystery",
        "fortune": "Your headphones will spontaneously develop complex knots that defy the laws of physics and patience.",
        "symbol": "🎧",
        "color": "#00b894"
    },
    {
        "card": "The Shopping List Vanishing Act",
        "fortune": "You will remember everything on your shopping list except the one item you specifically went to the store to buy.",
        "symbol": "📝",
        "color": "#e17055"
    },
    {
        "card": "The USB Flip Paradox",
        "fortune": "USB cables will require a minimum of three insertion attempts, with the first two always being upside down.",
        "symbol": "🔌",
        "color": "#74b9ff"
    },
    {
        "card": "The Email Send Regret",
        "fortune": "You will notice typos in important emails exactly 0.3 seconds after clicking send, but never before.",
        "symbol": "📧",
        "color": "#fd63a3"
    },
    {
        "card": "The Food Delivery Delay",
        "fortune": "Your food delivery will arrive precisely when you've given up hope and started making a sandwich.",
        "symbol": "🍕",
        "color": "#ffeaa7"
    },
    {
        "card": "The Pen Ink Depletion",
        "fortune": "Every pen will run out of ink mid-signature on important documents, forcing you to scribble desperately.",
        "symbol": "🖋️",
        "color": "#81ecec"
    },
    {
        "card": "The Weather App Deception",
        "fortune": "Weather forecasts will be accurate for everywhere except the exact 5-foot radius around your current location.",
        "symbol": "🌦️",
        "color": "#55a3ff"
    },
    {
        "card": "The Meeting Timezone Confusion",
        "fortune": "You will arrive fashionably early to virtual meetings that don't exist and fashionably late to ones that do.",
        "symbol": "💻",
        "color": "#ff7675"
    },
    {
        "card": "The Password Memory Lapse",
        "fortune": "You will remember passwords for accounts you haven't used in years but forget the one you use daily.",
        "symbol": "🔐",
        "color": "#00cec9"
    },
    {
        "card": "The Vending Machine Vendetta",
        "fortune": "Vending machines will accept your money enthusiastically but develop sudden commitment issues when dispensing snacks.",
        "symbol": "🥤",
        "color": "#fdcb6e"
    },
    {
        "card": "The Update Notification Persistence",
        "fortune": "Software update notifications will multiply when ignored, eventually achieving sentience and forming a union.",
        "symbol": "🔄",
        "color": "#e84393"
    }
]

@useless_fortune.route('/')
def index():
    """Main fortune telling page"""
    # Initialize session variables if they don't exist
    if 'useless_fortune_cards_drawn' not in session:
        session['useless_fortune_cards_drawn'] = 0
    if 'useless_fortune_current_card' not in session:
        session['useless_fortune_current_card'] = None
    
    return render_template('useless_fortune.html.jinja2')

@useless_fortune.route('/draw-card')
def draw_card():
    """API endpoint to draw a random useless fortune card"""
    # Pick a random fortune
    fortune = random.choice(USELESS_FORTUNES)
    
    # Update session
    session['useless_fortune_cards_drawn'] = session.get('useless_fortune_cards_drawn', 0) + 1
    session['useless_fortune_current_card'] = fortune
    
    return jsonify({
        'success': True,
        'card': fortune,
        'total_drawn': session['useless_fortune_cards_drawn']
    })

@useless_fortune.route('/reset')
def reset_session():
    """Reset the fortune session"""
    session.pop('useless_fortune_cards_drawn', None)
    session.pop('useless_fortune_current_card', None)
    
    return jsonify({
        'success': True,
        'message': 'Fortune session reset'
    })