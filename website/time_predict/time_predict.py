from flask import Blueprint, render_template, request, session, jsonify
import time
import json

# Create blueprint with template folder
time_predict = Blueprint('time_predict', __name__, template_folder='templates')

def get_session_keys(mode):
    """
    Generate session keys for a specific mode to keep statistics separate.
    
    Args:
        mode (str): Either 'predict' or 'react'
    
    Returns:
        dict: Dictionary containing session key names for the mode
    """
    prefix = f'time_predict_{mode}'
    return {
        'start_time': f'{prefix}_start_time',
        'game_active': f'{prefix}_game_active',
        'best_score': f'{prefix}_best_score',
        'games_played': f'{prefix}_games_played',
        'wins': f'{prefix}_wins'
    }

def get_win_threshold(mode):
    """
    Get the win threshold for a specific mode.
    
    Args:
        mode (str): Either 'predict' or 'react'
    
    Returns:
        float: Win threshold in seconds
    """
    thresholds = {
        'predict': 0.1,  # 0.1 seconds tolerance for predict mode
        'react': 0.05    # 0.05 seconds tolerance for react mode
    }
    return thresholds.get(mode, 0.05)

@time_predict.route('/')
def index():
    """
    Main route for the time prediction game.
    Displays the welcome screen with game instructions and mode selection.
    """
    # Initialize session variables for both modes if they don't exist
    for mode in ['predict', 'react']:
        keys = get_session_keys(mode)
        session[keys['start_time']] = None
        session[keys['game_active']] = False
        
        # Initialize stats if they don't exist
        if keys['best_score'] not in session:
            session[keys['best_score']] = None
        if keys['games_played'] not in session:
            session[keys['games_played']] = 0
        if keys['wins'] not in session:
            session[keys['wins']] = 0
    
    return render_template('time_predict.html')

@time_predict.route('/get_stats')
def get_stats():
    """
    API endpoint to get statistics for a specific mode.
    """
    try:
        mode = request.args.get('mode', 'predict')
        if mode not in ['predict', 'react']:
            return jsonify({
                'success': False,
                'error': 'Invalid mode'
            }), 400
        
        keys = get_session_keys(mode)
        
        stats = {
            'games_played': session.get(keys['games_played'], 0),
            'best_score': session.get(keys['best_score']),
            'wins': session.get(keys['wins'], 0)
        }
        
        return jsonify({
            'success': True,
            'stats': stats,
            'mode': mode
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@time_predict.route('/start_game', methods=['POST'])
def start_game():
    """
    API endpoint to start a new game.
    Records the start time and activates the game for the specified mode.
    """
    try:
        data = request.get_json() or {}
        mode = data.get('mode', 'predict')
        
        if mode not in ['predict', 'react']:
            return jsonify({
                'success': False,
                'error': 'Invalid mode'
            }), 400
        
        keys = get_session_keys(mode)
        
        # Record the precise start time
        start_time = time.time()
        session[keys['start_time']] = start_time
        session[keys['game_active']] = True
        
        return jsonify({
            'success': True,
            'start_time': start_time,
            'mode': mode,
            'message': f'Game started in {mode} mode! Press SPACE when you think 10 seconds have passed.'
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
        data = request.get_json() or {}
        mode = data.get('mode', 'predict')
        
        if mode not in ['predict', 'react']:
            return jsonify({
                'success': False,
                'error': 'Invalid mode'
            }), 400
        
        keys = get_session_keys(mode)
        
        if not session.get(keys['game_active'], False):
            return jsonify({
                'success': False,
                'error': f'No active {mode} game found'
            }), 400
        
        # Get the current time and calculate elapsed time
        end_time = time.time()
        start_time = session.get(keys['start_time'])
        
        if start_time is None:
            return jsonify({
                'success': False,
                'error': 'Start time not found'
            }), 400
        
        elapsed_time = end_time - start_time
        target_time = 10.0  # Target is exactly 10 seconds
        difference = elapsed_time - target_time
        
        # Get win threshold for this mode
        win_threshold = get_win_threshold(mode)
        is_winner = abs(difference) <= win_threshold
        
        # Update statistics for this mode
        session[keys['games_played']] = session.get(keys['games_played'], 0) + 1
        
        if is_winner:
            session[keys['wins']] = session.get(keys['wins'], 0) + 1
        
        current_best = session.get(keys['best_score'])
        
        # Best score is the smallest absolute difference
        if current_best is None or abs(difference) < abs(current_best):
            session[keys['best_score']] = difference
        
        # Deactivate the game
        session[keys['game_active']] = False
        
        # Create result message
        if difference > 0:
            timing_message = f"You were {difference:.3f} seconds LATE"
        elif difference < 0:
            timing_message = f"You were {abs(difference):.3f} seconds EARLY"
        else:
            timing_message = "PERFECT TIMING!"
        
        # Prepare updated statistics
        stats = {
            'games_played': session[keys['games_played']],
            'best_score': session.get(keys['best_score']),
            'wins': session.get(keys['wins'], 0)
        }
        
        return jsonify({
            'success': True,
            'elapsed_time': round(elapsed_time, 3),
            'target_time': target_time,
            'difference': round(difference, 3),
            'is_winner': is_winner,
            'timing_message': timing_message,
            'win_threshold': win_threshold,
            'mode': mode,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@time_predict.route('/reset_stats', methods=['POST'])
def reset_stats():
    """
    API endpoint to reset player statistics for a specific mode.
    """
    try:
        data = request.get_json() or {}
        mode = data.get('mode', 'predict')
        
        if mode not in ['predict', 'react']:
            return jsonify({
                'success': False,
                'error': 'Invalid mode'
            }), 400
        
        keys = get_session_keys(mode)
        
        # Reset all statistics for this mode
        session[keys['best_score']] = None
        session[keys['games_played']] = 0
        session[keys['wins']] = 0
        session[keys['game_active']] = False
        session[keys['start_time']] = None
        
        return jsonify({
            'success': True,
            'message': f'{mode.capitalize()} mode statistics reset successfully',
            'mode': mode
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@time_predict.route('/get_all_stats')
def get_all_stats():
    """
    API endpoint to get statistics for both modes.
    Useful for debugging or showing combined statistics.
    """
    try:
        all_stats = {}
        
        for mode in ['predict', 'react']:
            keys = get_session_keys(mode)
            all_stats[mode] = {
                'games_played': session.get(keys['games_played'], 0),
                'best_score': session.get(keys['best_score']),
                'wins': session.get(keys['wins'], 0),
                'win_threshold': get_win_threshold(mode)
            }
        
        return jsonify({
            'success': True,
            'stats': all_stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500