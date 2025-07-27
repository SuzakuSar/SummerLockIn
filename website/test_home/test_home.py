"""
Enhanced Test Homepage Blueprint for SUMMERLOCKIN Project
Features a scrollable game collection with viral engagement features
Designed for easy maintenance and game additions with user progress tracking
"""

from flask import Blueprint, render_template, jsonify, request, session
import json
from collections import defaultdict

# Create blueprint with template folder
test_home = Blueprint('test_home', __name__, template_folder='templates')

# ===== GAMES CONFIGURATION =====
# Easy to maintain - just add new games to this list!
GAMES_DATA = [
    # Mood/Pages
    {
        'name': 'Excited Page',
        'description': 'Feel the cosmic energy and excitement!',
        'endpoint': 'helloWorld.hello_World',
        'icon': '🌟',
        'category': 'mood',
        'tags': ['mood', 'excited', 'energy', 'happy'],
        'difficulty': 1
    },
    {
        'name': 'Nonchalant Page', 
        'description': 'Cool and collected vibes',
        'endpoint': 'helloWorld.sup_World',
        'icon': '🌙',
        'category': 'mood',
        'tags': ['mood', 'nonchalant', 'cool', 'chill'],
        'difficulty': 1
    },
    
    # Clicker/Incremental
    {
        'name': 'Clicker Game',
        'description': 'Click to build your cosmic empire',
        'endpoint': 'clicker_game.index',
        'icon': '🛸',
        'category': 'clicker',
        'tags': ['clicker', 'incremental', 'empire', 'cosmic'],
        'difficulty': 2
    },
    
    # Entertainment/Fun
    {
        'name': 'Random Jokes',
        'description': 'Stellar humor from across the galaxy',
        'endpoint': 'random_jokes.index',
        'icon': '⭐',
        'category': 'entertainment',
        'tags': ['jokes', 'humor', 'funny', 'entertainment', 'comedy'],
        'difficulty': 1
    },
    {
        'name': 'Do Not Click',
        'description': 'Resist the forbidden button... if you can',
        'endpoint': 'do_not_click.index',
        'icon': '⚠️',
        'category': 'entertainment',
        'tags': ['forbidden', 'button', 'temptation', 'warning'],
        'difficulty': 2
    },
    {
        'name': 'Fake Download',
        'description': 'Simulate classified file access',
        'endpoint': 'fake_download.index',
        'icon': '📁',
        'category': 'entertainment',
        'tags': ['fake', 'download', 'files', 'simulation'],
        'difficulty': 1
    },
    {
        'name': 'Fake Chatbot',
        'description': 'Converse with artificial minds',
        'endpoint': 'fake_chatbot.index',
        'icon': '🤖',
        'category': 'entertainment',
        'tags': ['chatbot', 'ai', 'conversation', 'artificial'],
        'difficulty': 2
    },
    {
        'name': 'Lucky Lever',
        'description': 'Pull for cosmic fortune and chance',
        'endpoint': 'lucky_lever.index',
        'icon': '🎰',
        'category': 'entertainment',
        'tags': ['luck', 'chance', 'lever', 'fortune', 'random'],
        'difficulty': 1
    },
    {
        'name': 'Useless Fortune',
        'description': 'Cosmic tarot predictions and mysticism',
        'endpoint': 'useless_fortune.index',
        'icon': '🔮',
        'category': 'entertainment',
        'tags': ['fortune', 'tarot', 'prediction', 'mysticism'],
        'difficulty': 1
    },
    {
        'name': 'Coin Flip',
        'description': 'Simple random chance generator',
        'endpoint': 'coin_flip.index',
        'icon': '🪙',
        'category': 'entertainment',
        'tags': ['coin', 'flip', 'random', 'chance'],
        'difficulty': 1
    },
    {
        'name': 'Prank Helper',
        'description': 'Cosmic mischief assistance tools',
        'endpoint': 'prank_helper.index',
        'icon': '😈',
        'category': 'entertainment',
        'tags': ['prank', 'mischief', 'jokes', 'tricks'],
        'difficulty': 2
    },
    
    # Puzzles/Brain Games
    {
        'name': 'Guessing Game',
        'description': 'Test your psychic prediction powers',
        'endpoint': 'guessing_game.index',
        'icon': '🎯',
        'category': 'puzzle',
        'tags': ['guessing', 'numbers', 'prediction', 'logic'],
        'difficulty': 3
    },
    {
        'name': 'Block Blast',
        'description': 'Tetris-style puzzle madness',
        'endpoint': 'block_blast.index',
        'icon': '🔳',
        'category': 'puzzle',
        'tags': ['tetris', 'blocks', 'puzzle', 'strategy'],
        'difficulty': 4
    },
    {
        'name': 'Space Cargo Manager',
        'description': 'Organize cosmic deliveries with drag & drop',
        'endpoint': 'drag_drop.index',
        'icon': '📦',
        'category': 'puzzle',
        'tags': ['drag', 'drop', 'cargo', 'organization'],
        'difficulty': 3
    },
    {
        'name': 'Wire Matching',
        'description': 'Connect the electrical circuits',
        'endpoint': 'wire_matching.index',
        'icon': '🔌',
        'category': 'puzzle',
        'tags': ['wires', 'circuits', 'electrical', 'matching'],
        'difficulty': 4
    },
    {
        'name': 'Number Sequence',
        'description': 'Follow the mathematical patterns',
        'endpoint': 'number_sequence.index',
        'icon': '🔢',
        'category': 'puzzle',
        'tags': ['numbers', 'sequence', 'math', 'pattern'],
        'difficulty': 3
    },
    {
        'name': 'Space Door Control',
        'description': 'Manage airlock security systems',
        'endpoint': 'door_game.index',
        'icon': '🚪',
        'category': 'puzzle',
        'tags': ['doors', 'airlock', 'security', 'control'],
        'difficulty': 3
    },
    {
        'name': 'I Spy Game',
        'description': 'Find hidden cosmic objects',
        'endpoint': 'i_spy.index',
        'icon': '🔍',
        'category': 'puzzle',
        'tags': ['spy', 'find', 'hidden', 'search'],
        'difficulty': 2
    },
    {
        'name': 'Connect Dots',
        'description': 'Link celestial connection points',
        'endpoint': 'connect_dots.index',
        'icon': '🔗',
        'category': 'puzzle',
        'tags': ['connect', 'dots', 'lines', 'pattern'],
        'difficulty': 3
    },
    {
        'name': 'Balance Scale Game',
        'description': 'Master physics and equilibrium',
        'endpoint': 'balance_scale.index',
        'icon': '⚖️',
        'category': 'puzzle',
        'tags': ['balance', 'scale', 'physics', 'weight'],
        'difficulty': 4
    },
    {
        'name': 'Lockpick Game',
        'description': 'Master the art of lock manipulation',
        'endpoint': 'lockpick_game.index',
        'icon': '🔓',
        'category': 'puzzle',
        'tags': ['lockpick', 'locks', 'security', 'skill'],
        'difficulty': 5
    },
    {
        'name': '2048 - Space Edition',
        'description': 'Combine numbers in cosmic style',
        'endpoint': 'game_2048.index',
        'icon': '🎲',
        'category': 'puzzle',
        'tags': ['2048', 'numbers', 'combination', 'strategy'],
        'difficulty': 4
    },
    {
        'name': 'Space Maze Navigator',
        'description': 'Navigate through cosmic labyrinths',
        'endpoint': 'maze_game.index',
        'icon': '🚀',
        'category': 'puzzle',
        'tags': ['maze', 'navigation', 'labyrinth', 'space'],
        'difficulty': 3
    },
    
    # Word Games
    {
        'name': 'Hangman',
        'description': 'Word guessing in the dark void',
        'endpoint': 'hangman.index',
        'icon': '🔮',
        'category': 'word',
        'tags': ['hangman', 'words', 'guessing', 'vocabulary'],
        'difficulty': 3
    },
    {
        'name': 'Space Wordle',
        'description': 'Word puzzles from distant worlds',
        'endpoint': 'wordle.index',
        'icon': '🔤',
        'category': 'word',
        'tags': ['wordle', 'words', 'puzzle', 'letters'],
        'difficulty': 4
    },
    {
        'name': 'Story Generator',
        'description': 'Create galactic adventures with words',
        'endpoint': 'story_generator.index',
        'icon': '📖',
        'category': 'creative',
        'tags': ['story', 'creative', 'writing', 'adventure'],
        'difficulty': 2
    },
    
    # Skill/Timing Games
    {
        'name': 'Time Predict Challenge',
        'description': 'Test your internal clock - hit exactly 10.000 seconds!',
        'endpoint': 'time_predict.index',
        'icon': '🕒',
        'category': 'skill',
        'tags': ['time', 'timing', 'predict', 'precision', '10 seconds', 'challenge'],
        'difficulty': 4
    },
    {
        'name': 'Typing Test',
        'description': 'Measure your keyboard velocity',
        'endpoint': 'typing_test.index',
        'icon': '⌨️',
        'category': 'skill',
        'tags': ['typing', 'speed', 'keyboard', 'wpm'],
        'difficulty': 3
    },
    {
        'name': 'Click Speed Calculator',
        'description': 'Test your clicking prowess',
        'endpoint': 'click_speed.index',
        'icon': '⚡',
        'category': 'skill',
        'tags': ['click', 'speed', 'fast', 'reaction'],
        'difficulty': 2
    },
    {
        'name': 'Shell Game',
        'description': 'Follow the cosmic cup challenge',
        'endpoint': 'shell_game.index',
        'icon': '🎪',
        'category': 'skill',
        'tags': ['shell', 'follow', 'tracking', 'attention'],
        'difficulty': 4
    },
    {
        'name': 'OSU! Clone',
        'description': 'Rhythm clicking mastery',
        'endpoint': 'osu_game.index',
        'icon': '🎯',
        'category': 'skill',
        'tags': ['osu', 'rhythm', 'clicking', 'music'],
        'difficulty': 5
    },
    {
        'name': 'Bomb Defuser',
        'description': 'Disarm explosive devices under pressure',
        'endpoint': 'bomb_defuse.index',
        'icon': '💣',
        'category': 'skill',
        'tags': ['bomb', 'defuse', 'pressure', 'danger'],
        'difficulty': 5
    },
    {
        'name': 'Slider Challenge',
        'description': 'Master precision control systems',
        'endpoint': 'slider_challenge.index',
        'icon': '🎚️',
        'category': 'skill',
        'tags': ['slider', 'precision', 'control', 'accuracy'],
        'difficulty': 4
    },
    {
        'name': 'Speed Sort Challenge',
        'description': 'Sort items at lightning speed',
        'endpoint': 'speed_sort.index',
        'icon': '⚡',
        'category': 'skill',
        'tags': ['sort', 'speed', 'organize', 'fast'],
        'difficulty': 4
    },
    {
        'name': 'One-Pixel Hunt',
        'description': 'Find the needle in the digital haystack',
        'endpoint': 'one_pixel_hunt.index',
        'icon': '🔍',
        'category': 'skill',
        'tags': ['pixel', 'hunt', 'precision', 'find'],
        'difficulty': 5
    },
    
    # Arcade/Action Games
    {
        'name': 'Cosmic Dino Runner',
        'description': 'Chrome dinosaur game in space - jump over obstacles!',
        'endpoint': 'dino_runner.index',
        'icon': '🦕',
        'category': 'arcade',
        'tags': ['dino', 'runner', 'jumping', 'endless', 'chrome', 'obstacles', 'classic'],
        'difficulty': 3
    },
    {
        'name': 'Snake Game',
        'description': 'Classic serpent navigation challenge',
        'endpoint': 'snake_game.index',
        'icon': '🐍',
        'category': 'arcade',
        'tags': ['snake', 'classic', 'navigation', 'grow'],
        'difficulty': 3
    },
    {
        'name': 'Click Clear Game',
        'description': 'Clean up the cosmic debris field',
        'endpoint': 'click_clear.index',
        'icon': '💫',
        'category': 'arcade',
        'tags': ['click', 'clear', 'cleanup', 'debris'],
        'difficulty': 2
    },
    {
        'name': 'Space Invaders',
        'description': 'Classic alien shooting action',
        'endpoint': 'space_invaders.index',
        'icon': '🛸',
        'category': 'arcade',
        'tags': ['space', 'invaders', 'shooting', 'aliens'],
        'difficulty': 4
    },
    {
        'name': 'Brick Breaker Game',
        'description': 'Smash through cosmic barriers',
        'endpoint': 'brick_breaker.index',
        'icon': '🧱',
        'category': 'arcade',
        'tags': ['brick', 'breaker', 'ball', 'paddle'],
        'difficulty': 3
    },
    {
        'name': 'Cosmic Pong',
        'description': 'Interstellar paddle battle',
        'endpoint': 'pong.index',
        'icon': '🏓',
        'category': 'arcade',
        'tags': ['pong', 'paddle', 'ball', 'classic'],
        'difficulty': 3
    },
    {
        'name': 'Rage Slots',
        'description': 'High-intensity slot machine action',
        'endpoint': 'slots_machine.index',
        'icon': '🎰',
        'category': 'arcade',
        'tags': ['slots', 'machine', 'gambling', 'rage'],
        'difficulty': 2
    },
    
    # Strategy Games
    {
        'name': 'Tic Tac Toe',
        'description': 'Strategic grid warfare',
        'endpoint': 'tic_tac_toe.index',
        'icon': '⚡',
        'category': 'strategy',
        'tags': ['tic', 'tac', 'toe', 'grid', 'strategy'],
        'difficulty': 2
    },
    {
        'name': 'Rock Paper Scissors',
        'description': 'Ancient combat techniques',
        'endpoint': 'rock_paper_scissors.index',
        'icon': '⚔️',
        'category': 'strategy',
        'tags': ['rock', 'paper', 'scissors', 'battle'],
        'difficulty': 2
    },
    {
        'name': 'Space Pattern Memory',
        'description': 'Remember complex stellar sequences',
        'endpoint': 'space_memory_game.index',
        'icon': '🎴',
        'category': 'strategy',
        'tags': ['memory', 'pattern', 'sequence', 'cards'],
        'difficulty': 4
    },
    
    # Educational
    {
        'name': 'Mountain Academy',
        'description': 'Train your mathematical prowess',
        'endpoint': 'multiplication_trainer.index',
        'icon': '🏔️',
        'category': 'education',
        'tags': ['math', 'multiplication', 'training', 'academy'],
        'difficulty': 3
    },
    {
        'name': 'Coordinate Hunter',
        'description': 'Navigate mathematical coordinate space',
        'endpoint': 'coordinate_game.index',
        'icon': '🎯',
        'category': 'education',
        'tags': ['coordinates', 'math', 'navigation', 'points'],
        'difficulty': 4
    },
    
    # Health/Utility
    {
        'name': 'Water Tracker',
        'description': 'Monitor your hydration levels',
        'endpoint': 'water_drinker.index',
        'icon': '💧',
        'category': 'health',
        'tags': ['water', 'hydration', 'health', 'tracker'],
        'difficulty': 1
    },
    
    # Simulation
    {
        'name': "Lucky's Temperature Control",
        'description': 'Regulate your pet tortoise habitat',
        'endpoint': 'tortoise_temp.index',
        'icon': '🐢',
        'category': 'simulation',
        'tags': ['tortoise', 'temperature', 'pet', 'control'],
        'difficulty': 2
    },
]

# Categories for filtering (auto-generated from games data)
def get_categories():
    """Get all unique categories from games data"""
    categories = set()
    for game in GAMES_DATA:
        categories.add(game['category'])
    return sorted(list(categories))

def get_category_counts():
    """Get count of games per category"""
    counts = defaultdict(int)
    for game in GAMES_DATA:
        counts[game['category']] += 1
    return dict(counts)

def get_games_by_category(category=None):
    """Get games filtered by category"""
    if not category:
        return GAMES_DATA
    return [game for game in GAMES_DATA if game['category'] == category]

def search_games(query):
    """Search games by name, description, or tags"""
    if not query:
        return GAMES_DATA
    
    query = query.lower()
    results = []
    
    for game in GAMES_DATA:
        # Search in name
        if query in game['name'].lower():
            results.append(game)
            continue
            
        # Search in description
        if query in game['description'].lower():
            results.append(game)
            continue
            
        # Search in tags
        if any(query in tag.lower() for tag in game['tags']):
            results.append(game)
            continue
    
    return results

def get_mock_user_stats():
    """Generate mock user statistics for demonstration"""
    # In production, this would come from a database or session
    return {
        'games_played': 12,
        'achievements': 5,
        'play_time': '2h 34m',
        'streak': 3,
        'last_login': None,
        'favorite_category': 'arcade'
    }

# ===== ROUTES =====

@test_home.route('/')
def index():
    """
    Main test homepage route - displays enhanced viral game collection
    """
    categories = get_categories()
    category_counts = get_category_counts()
    
    # Get optional parameters from URL
    selected_category = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    # Filter games based on parameters
    if search_query:
        games = search_games(search_query)
    else:
        games = get_games_by_category(selected_category if selected_category else None)
    
    # Add popup data to each game
    for i, game in enumerate(games):
        game['popup_id'] = f"popup-{i}"
        game['card_id'] = f"card-{i}"
        game['index'] = i
    
    # Get user statistics (mock data for now)
    user_stats = get_mock_user_stats()
    
    return render_template('test_home.html.jinja2',
                         games=games,
                         categories=categories,
                         category_counts=category_counts,
                         selected_category=selected_category,
                         search_query=search_query,
                         total_games=len(GAMES_DATA),
                         user_stats=user_stats)

@test_home.route('/api/search')
def api_search():
    """
    API endpoint for live search functionality
    """
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    # Apply filters
    if query:
        games = search_games(query)
    else:
        games = get_games_by_category(category if category else None)
    
    # Add popup data to each game for API response
    for i, game in enumerate(games):
        game['popup_id'] = f"popup-{i}"
        game['card_id'] = f"card-{i}" 
        game['index'] = i
    
    return jsonify({
        'success': True,
        'games': games,
        'count': len(games),
        'query': query,
        'category': category
    })

@test_home.route('/api/categories')
def api_categories():
    """
    API endpoint to get all categories with counts
    """
    return jsonify({
        'success': True,
        'categories': get_categories(),
        'category_counts': get_category_counts()
    })

@test_home.route('/api/user/stats')
def api_user_stats():
    """
    API endpoint to get user statistics
    """
    return jsonify({
        'success': True,
        'stats': get_mock_user_stats()
    })

@test_home.route('/stats')
def stats():
    """
    Show statistics about the game collection
    """
    categories = get_categories()
    category_counts = get_category_counts()
    
    stats_data = {
        'total_games': len(GAMES_DATA),
        'total_categories': len(categories),
        'category_breakdown': category_counts,
        'difficulty_breakdown': {},
        'average_difficulty': 0
    }
    
    # Calculate difficulty breakdown
    difficulty_counts = defaultdict(int)
    total_difficulty = 0
    
    for game in GAMES_DATA:
        difficulty = game.get('difficulty', 3)
        difficulty_counts[difficulty] += 1
        total_difficulty += difficulty
    
    stats_data['difficulty_breakdown'] = dict(difficulty_counts)
    stats_data['average_difficulty'] = round(total_difficulty / len(GAMES_DATA), 1)
    
    return jsonify({
        'success': True,
        'stats': stats_data
    })

# ===== HELPER FUNCTIONS FOR EASY MAINTENANCE =====

def add_game(name, description, endpoint, icon, category, tags, difficulty=3):
    """
    Helper function to easily add new games
    (For future use - games should be added to GAMES_DATA list above)
    """
    new_game = {
        'name': name,
        'description': description,
        'endpoint': endpoint,
        'icon': icon,
        'category': category,
        'tags': tags if isinstance(tags, list) else [tags],
        'difficulty': difficulty
    }
    return new_game

def validate_game_data():
    """
    Validate that all games have required fields
    """
    required_fields = ['name', 'description', 'endpoint', 'icon', 'category', 'tags']
    
    for i, game in enumerate(GAMES_DATA):
        for field in required_fields:
            if field not in game:
                print(f"Warning: Game {i} missing field '{field}': {game.get('name', 'Unknown')}")
        
        # Validate tags is a list
        if not isinstance(game.get('tags', []), list):
            print(f"Warning: Game '{game.get('name', 'Unknown')}' tags should be a list")
        
        # Set default difficulty if missing
        if 'difficulty' not in game:
            game['difficulty'] = 3

# Run validation on import (for development)
if __name__ == '__main__':
    validate_game_data()        