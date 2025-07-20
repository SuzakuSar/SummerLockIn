from flask import Blueprint, render_template, session, request, jsonify

# Create blueprint with template folder
snake_game = Blueprint('snake_game', __name__, template_folder='templates')

@snake_game.route('/')
def index():
    """Snake game main page with canvas and controls"""
    # Initialize high score if not exists
    if 'snake_high_score' not in session:
        session['snake_high_score'] = 0
    
    return render_template('snake_game.html', high_score=session['snake_high_score'])

@snake_game.route('/score', methods=['POST'])
def update_score():
    """Update high score if new score is higher"""
    try:
        new_score = int(request.json.get('score', 0))
        current_high = session.get('snake_high_score', 0)
        
        if new_score > current_high:
            session['snake_high_score'] = new_score
            return jsonify({'new_high': True, 'high_score': new_score})
        
        return jsonify({'new_high': False, 'high_score': current_high})
    
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid score'}), 400

@snake_game.route('/reset')
def reset_score():
    """Reset high score for testing purposes"""
    session['snake_high_score'] = 0
    return jsonify({'message': 'High score reset', 'high_score': 0})