# ===== FILE: website/analytics/analytics.py =====
from flask import Blueprint, request, session, jsonify, render_template
import json
import os
from datetime import datetime

# Create the blueprint (just like clicker_game.py, hangman.py, etc.)
analytics = Blueprint('analytics', __name__, template_folder='templates')

# ===== PRODUCTION-READY FILE HANDLING =====

def get_stats_file_path():
    """Production-ready file path"""
    # Check if we're on Render.com (your hosting platform)
    if os.environ.get('RENDER'):
        data_dir = '/opt/render/project/data'
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'game_stats.json')
    else:
        return 'game_stats.json'  # Local development

def load_game_stats():
    """Load stats with production safety"""
    stats_file = get_stats_file_path()
    try:
        with open(stats_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Starting fresh stats file")
        return {}
    except Exception as e:
        print(f"Error loading stats: {e}")
        return {}

def save_game_stats(stats):
    """Save stats with production safety"""
    stats_file = get_stats_file_path()
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(stats_file), exist_ok=True)
        
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving stats: {e}")
        return False

# ===== GAME TRACKING LOGIC =====

def track_game_visit(path):
    """Track unique game sessions - production ready"""
    
    # COMPLETE game mapping - just add new games here with one line
    game_mapping = {
        # Original games
        '/clickergame': 'Clicker Game',
        '/randomjokes': 'Random Jokes',
        '/guessinggame': 'Guessing Game',
        '/hangman': 'Hangman',
        '/timepredict': 'Time Predict',
        '/spacememory': 'Space Memory',
        
        # All your other games
        '/mountainacademy': 'Multiplication Trainer',
        '/dino-runner': 'Dino Runner',
        '/snakegame': 'Snake Game',
        '/tictactoe': 'Tic Tac Toe',
        '/rockpaperscissors': 'Rock Paper Scissors',
        '/blockblast': 'Block Blast',
        '/wordle': 'Wordle',
        '/typingtest': 'Typing Test',
        '/clickspeed': 'Click Speed Test',
        '/dragdrop': 'Drag & Drop',
        '/shellgame': 'Shell Game',
        '/wirematching': 'Wire Matching',
        '/donotclick': 'Do Not Click',
        '/clickclear': 'Click Clear',
        '/numbersequence': 'Number Sequence',
        '/fakedownload': 'Fake Download',
        '/door': 'Door Game',
        '/fakechatbot': 'Fake Chatbot',
        '/osu': 'OSU Game',
        '/luckylever': 'Lucky Lever',
        '/tortoise_temp': 'Tortoise Temperature',
        '/uselessfortune': 'Useless Fortune',
        '/bombdefuse': 'Bomb Defuse',
        '/waterdrinker': 'Water Drinker',
        '/space-invaders': 'Space Invaders',
        '/brickbreaker': 'Brick Breaker',
        '/coinflip': 'Coin Flip',
        '/ispy': 'I Spy',
        '/storygenerator': 'Story Generator',
        '/coordinategame': 'Coordinate Game',
        '/slider_challenge': 'Slider Challenge',
        '/prankhelper': 'Prank Helper',
        '/pong': 'Pong',
        '/maze': 'Maze Game',
        '/game2048': '2048',
        '/balancescale': 'Balance Scale',
        '/spacememorygame': 'Space Memory Game',
        '/connect-dots': 'Connect Dots',
        '/speedsort': 'Speed Sort',
        '/lockpick': 'Lockpick Game',
        '/pixelhunt': 'One Pixel Hunt',
        '/slots': 'Slots Machine',
        
        # TO ADD NEW GAMES: Just add one line like this:
        # '/newgame': 'My New Game Name',
    }
    
    # Find matching game
    for url_prefix, game_name in game_mapping.items():
        if path.startswith(url_prefix):
            session_key = f'visited_{game_name.replace(" ", "_").replace("&", "and").lower()}'
            
            # Only count once per session
            if session_key not in session:
                session[session_key] = True
                session.permanent = True
                
                # PRODUCTION-READY: Load stats with safety
                stats = load_game_stats()
                
                # Simple stats structure
                if game_name not in stats:
                    stats[game_name] = {
                        'unique_sessions': 0,
                        'first_seen': datetime.now().strftime('%Y-%m-%d'),
                        'last_played': datetime.now().strftime('%Y-%m-%d')
                    }
                
                # Update stats
                stats[game_name]['unique_sessions'] += 1
                stats[game_name]['last_played'] = datetime.now().strftime('%Y-%m-%d')
                
                # PRODUCTION-READY: Save with safety
                if save_game_stats(stats):
                    print(f"🎮 TRACKED: New session for {game_name} (Total: {stats[game_name]['unique_sessions']})")
                else:
                    print(f"⚠️ WARNING: Failed to save stats for {game_name}")
                
                return True
            else:
                print(f"🎮 EXISTING: Session already counted for {game_name}")
                return False
    return False

def auto_track_from_request(request_obj):
    """Function to be called from app.py"""
    if request_obj.method == 'GET':
        return track_game_visit(request_obj.path)
    return False

def process_stats_for_template(stats):
    """Process raw stats into template-ready format"""
    if not stats:
        return None, 0, 0, 0
    
    sorted_games = sorted(stats.items(), key=lambda x: x[1]['unique_sessions'], reverse=True)
    total_sessions = sum(game['unique_sessions'] for game in stats.values())
    total_games = len(stats)
    avg_sessions = total_sessions // total_games if total_games > 0 else 0
    
    # Get max sessions for progress bar calculation
    max_sessions = sorted_games[0][1]['unique_sessions'] if sorted_games else 1
    
    # Prepare games data for template
    games_data = []
    for i, (game_name, game_data) in enumerate(sorted_games):
        sessions = game_data['unique_sessions']
        percentage = round((sessions / total_sessions * 100), 1) if total_sessions > 0 else 0
        progress_width = round((sessions / max_sessions * 100), 1) if max_sessions > 0 else 0
        
        games_data.append({
            'name': game_name,
            'sessions': sessions,
            'percentage': f"{percentage:.1f}",
            'progress_width': progress_width,
            'last_played': game_data['last_played']
        })
    
    return games_data, total_sessions, total_games, avg_sessions

# Custom template filter for comma formatting
@analytics.app_template_filter('comma')
def comma_filter(value):
    """Add commas to numbers for better readability"""
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value

# ===== ANALYTICS ROUTES =====

@analytics.route('/')
def index():
    """Main analytics dashboard"""
    stats = load_game_stats()
    
    if not stats:
        return render_template('no_stats.html.jinja2')
    
    games_data, total_sessions, total_games, avg_sessions = process_stats_for_template(stats)
    
    return render_template('analytics.html.jinja2',
                         games=games_data,
                         total_sessions=total_sessions,
                         total_games=total_games,
                         avg_sessions=avg_sessions,
                         current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@analytics.route('/quick')
def quick():
    """Quick stats view"""
    stats = load_game_stats()
    
    if not stats:
        return render_template('no_stats.html.jinja2')
    
    games_data, total_sessions, total_games, avg_sessions = process_stats_for_template(stats)
    
    # Get top 10
    top_games = games_data[:10] if games_data else []
    
    return render_template('quick_stats.html.jinja2',
                         games=top_games,
                         total_sessions=total_sessions,
                         total_games=total_games)

@analytics.route('/api/stats')
def api_stats():
    """API endpoint for game statistics"""
    stats = load_game_stats()
    
    if not stats:
        return jsonify({'error': 'No stats available'})
    
    # Format for API
    api_data = {
        'total_games': len(stats),
        'total_sessions': sum(game['unique_sessions'] for game in stats.values()),
        'games': [
            {
                'rank': i + 1,
                'name': name,
                'sessions': data['unique_sessions'],
                'last_played': data['last_played'],
                'first_seen': data['first_seen']
            }
            for i, (name, data) in enumerate(
                sorted(stats.items(), key=lambda x: x[1]['unique_sessions'], reverse=True)
            )
        ]
    }
    
    return jsonify(api_data)

@analytics.route('/api/track')
def api_track():
    """API endpoint for manual tracking (if needed)"""
    game_name = request.args.get('game')
    if game_name:
        return jsonify({'status': 'received', 'game': game_name})
    return jsonify({'status': 'error', 'message': 'No game specified'})

@analytics.route('/reset')
def reset_stats():
    """Reset all stats (for testing - remove in production)"""
    stats_file = get_stats_file_path()
    try:
        if os.path.exists(stats_file):
            os.remove(stats_file)
        return jsonify({'status': 'success', 'message': 'Stats reset'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})