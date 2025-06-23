from flask import Blueprint, render_template, request, session, jsonify
import time
import json

# Create blueprint with template folder
time_predict = Blueprint('time_predict', __name__, template_folder='templates')

@time_predict.route('/')
def index():
    """
    Main route for the time prediction game.
    Displays the welcome screen with game instructions.
    """
    # Initialize session variables for this game
    session['time_predict_start_time'] = None
    session['time_predict_game_active'] = False
    session['time_predict_best_score'] = session.get('time_predict_best_score', None)
    session['time_predict_games_played'] = session.get('time_predict_games_played', 0)
    
    return render_template('time_predict.html')

@time_predict.route('/start_game', methods=['POST'])
def start_game():
    """
    API endpoint to start a new game.
    Records the start time and activates the game.
    """
    try:
        # Record the precise start time
        start_time = time.time()
        session['time_predict_start_time'] = start_time
        session['time_predict_game_active'] = True
        
        return jsonify({
            'success': True,
            'start_time': start_time,
            'message': 'Game started! Press SPACE when you think 10 seconds have passed.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@time_predict.route('/stop_game', methods=['POST'])
def stop_game():
    """
    API endpoint to stop the game and calculate results.
    Called when user presses spacebar.
    """
    try:
        if not session.get('time_predict_game_active', False):
            return jsonify({
                'success': False,
                'error': 'No active game found'
            }), 400
        
        # Get the current time and calculate elapsed time
        end_time = time.time()
        start_time = session.get('time_predict_start_time')
        
        if start_time is None:
            return jsonify({
                'success': False,
                'error': 'Start time not found'
            }), 400
        
        elapsed_time = end_time - start_time
        target_time = 10.0  # Target is exactly 10 seconds
        difference = elapsed_time - target_time
        
        # Determine if they won (within 0.05 seconds)
        win_threshold = 0.05
        is_winner = abs(difference) <= win_threshold
        
        # Update statistics
        session['time_predict_games_played'] = session.get('time_predict_games_played', 0) + 1
        current_best = session.get('time_predict_best_score')
        
        # Best score is the smallest absolute difference
        if current_best is None or abs(difference) < abs(current_best):
            session['time_predict_best_score'] = difference
        
        # Deactivate the game
        session['time_predict_game_active'] = False
        
        # Create result message
        if difference > 0:
            timing_message = f"You were {difference:.3f} seconds LATE"
        elif difference < 0:
            timing_message = f"You were {abs(difference):.3f} seconds EARLY"
        else:
            timing_message = "PERFECT TIMING!"
        
        return jsonify({
            'success': True,
            'elapsed_time': round(elapsed_time, 3),
            'target_time': target_time,
            'difference': round(difference, 3),
            'is_winner': is_winner,
            'timing_message': timing_message,
            'games_played': session['time_predict_games_played'],
            'best_score': session.get('time_predict_best_score'),
            'win_threshold': win_threshold
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@time_predict.route('/reset_stats', methods=['POST'])
def reset_stats():
    """
    API endpoint to reset player statistics.
    """
    try:
        session['time_predict_best_score'] = None
        session['time_predict_games_played'] = 0
        session['time_predict_game_active'] = False
        session['time_predict_start_time'] = None
        
        return jsonify({
            'success': True,
            'message': 'Statistics reset successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500