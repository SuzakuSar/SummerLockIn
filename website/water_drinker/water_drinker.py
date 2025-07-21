"""
WATER DRINKER SIMULATOR - FLASK BLUEPRINT
File Structure:
website/
├── water_drinker/
│   ├── __init__.py
│   ├── water_drinker.py
│   └── templates/
│       └── water_drinker.html

Remember to register this blueprint in website/__init__.py:
app.register_blueprint(water_drinker, url_prefix='/waterdrinker')
"""

# ====================
# File: website/water_drinker/water_drinker.py
# ====================

from flask import Blueprint, render_template, request, session, jsonify
from datetime import datetime

water_drinker = Blueprint('water_drinker', __name__, template_folder='templates')

# Daily water goal in mL
DAILY_GOAL = 2000  # 2 liters

# Cup sizes in mL
CUP_SIZES = {
    'small': 250,    # Small glass
    'medium': 350,   # Regular glass
    'large': 500,    # Large glass
    'bottle': 750    # Water bottle
}

@water_drinker.route('/')
def index():
    """Main water tracking page"""
    # Initialize session data if needed
    if 'water_intake' not in session:
        session['water_intake'] = 0
    
    if 'water_last_reset' not in session:
        session['water_last_reset'] = datetime.now().strftime('%Y-%m-%d')
    
    # Check if we need to reset for new day
    today = datetime.now().strftime('%Y-%m-%d')
    if session['water_last_reset'] != today:
        session['water_intake'] = 0
        session['water_last_reset'] = today
    
    # Calculate progress
    intake = session['water_intake']
    progress = min(100, (intake / DAILY_GOAL) * 100)
    
    # Hydration status
    if intake >= DAILY_GOAL:
        hydration_status = "Perfectly Hydrated! 💧"
        status_color = "#00ff88"
    elif intake >= DAILY_GOAL * 0.75:
        hydration_status = "Well Hydrated 💦"
        status_color = "#44aaff"
    elif intake >= DAILY_GOAL * 0.5:
        hydration_status = "Getting There 🌊"
        status_color = "#ffaa44"
    elif intake >= DAILY_GOAL * 0.25:
        hydration_status = "Need More Water 💧"
        status_color = "#ff8844"
    else:
        hydration_status = "Dehydrated! 🏜️"
        status_color = "#ff4444"
    
    return render_template('water_drinker.html.jinja2',
                         intake=intake,
                         goal=DAILY_GOAL,
                         progress=progress,
                         hydration_status=hydration_status,
                         status_color=status_color,
                         cup_sizes=CUP_SIZES)

@water_drinker.route('/drink', methods=['POST'])
def drink_water():
    """Add water intake"""
    try:
        cup_size = request.form.get('cup_size', 'medium')
        amount = CUP_SIZES.get(cup_size, 350)
        
        # Initialize if needed
        if 'water_intake' not in session:
            session['water_intake'] = 0
        
        # Add water
        session['water_intake'] += amount
        
        # Calculate new progress
        intake = session['water_intake']
        progress = min(100, (intake / DAILY_GOAL) * 100)
        
        return jsonify({
            'success': True,
            'intake': intake,
            'progress': progress,
            'amount_added': amount
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@water_drinker.route('/reset', methods=['POST'])
def reset_intake():
    """Reset daily water intake"""
    session['water_intake'] = 0
    session['water_last_reset'] = datetime.now().strftime('%Y-%m-%d')
    
    return jsonify({
        'success': True,
        'intake': 0,
        'progress': 0
    })

@water_drinker.route('/stats')
def get_stats():
    """Get current hydration stats"""
    intake = session.get('water_intake', 0)
    progress = min(100, (intake / DAILY_GOAL) * 100)
    
    return jsonify({
        'intake': intake,
        'goal': DAILY_GOAL,
        'progress': progress,
        'cups_drunk': intake // 250,  # Approximate cups
        'remaining': max(0, DAILY_GOAL - intake)
    })