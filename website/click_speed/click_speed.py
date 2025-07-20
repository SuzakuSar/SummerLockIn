# File: website/click_speed/click_speed.py
from flask import Blueprint, render_template, session, jsonify, request

click_speed = Blueprint('click_speed', __name__, template_folder='templates')

@click_speed.route('/')
def index():
    """Main clicking speed calculator page"""
    # Initialize session data if not exists
    if 'click_speed_personal_best' not in session:
        session['click_speed_personal_best'] = 0.0
    
    return render_template('click_speed.html', personal_best=session['click_speed_personal_best'])

@click_speed.route('/api/save_score', methods=['POST'])
def save_score():
    """Save the clicking speed score to session"""
    try:
        data = request.get_json()
        clicks_per_second = float(data.get('clicks_per_second', 0))
        
        # Update personal best if this score is better
        current_best = session.get('click_speed_personal_best', 0.0)
        if clicks_per_second > current_best:
            session['click_speed_personal_best'] = clicks_per_second
            session.permanent = True
            is_new_record = True
        else:
            is_new_record = False
        
        return jsonify({
            'success': True,
            'new_record': is_new_record,
            'personal_best': session['click_speed_personal_best']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@click_speed.route('/api/reset_best', methods=['POST'])
def reset_best():
    """Reset personal best score"""
    session['click_speed_personal_best'] = 0.0
    return jsonify({'success': True, 'personal_best': 0.0})