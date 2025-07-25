"""
Test Homepage Blueprint for SUMMERLOCKIN Project
Features a scrollable game collection with search functionality
Designed for easy maintenance and game additions
"""

from flask import Blueprint, render_template, jsonify, request
import json

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
        'tags': ['mood', 'excited', 'energy', 'happy']
    },
    {
        'name': 'Nonchalant Page', 
        'description': 'Cool and collected vibes',
        'endpoint': 'helloWorld.sup_World',
        'icon': '🌙',
        'category': 'mood',
        'tags': ['mood', 'nonchalant', 'cool', 'chill']
    },
    
    # Clicker/Incremental
    {
        'name': 'Clicker Game',
        'description': 'Click to build your cosmic empire',
        'endpoint': 'clicker_game.index',
        'icon': '🛸',
        'category': 'clicker',
        'tags': ['clicker', 'incremental', 'empire', 'cosmic']
    },
    
    # Entertainment/Fun
    {
        'name': 'Random Jokes',
        'description': 'Stellar humor from across the galaxy',
        'endpoint': 'random_jokes.index',
        'icon': '⭐',
        'category': 'entertainment',
        'tags': ['jokes', 'humor', 'funny', 'entertainment', 'comedy']
    },
    {
        'name': 'Do Not Click',
        'description': 'Resist the forbidden button... if you can',
        'endpoint': 'do_not_click.index',
        'icon': '⚠️',
        'category': 'entertainment',
        'tags': ['forbidden', 'button', 'temptation', 'warning']
    },
    {
        'name': 'Fake Download',
        'description': 'Simulate classified file access',
        'endpoint': 'fake_download.index',
        'icon': '📁',
        'category': 'entertainment',
        'tags': ['fake', 'download', 'files', 'simulation']
    },
    {
        'name': 'Fake Chatbot',
        'description': 'Converse with artificial minds',
        'endpoint': 'fake_chatbot.index',
        'icon': '🤖',
        'category': 'entertainment',
        'tags': ['chatbot', 'ai', 'conversation', 'artificial']
    },
    {
        'name': 'Lucky Lever',
        'description': 'Pull for cosmic fortune and chance',
        'endpoint': 'lucky_lever.index',
        'icon': '🎰',
        'category': 'entertainment',
        'tags': ['luck', 'chance', 'lever', 'fortune', 'random']
    },
    {
        'name': 'Useless Fortune',
        'description': 'Cosmic tarot predictions and mysticism',
        'endpoint': 'useless_fortune.index',
        'icon': '🔮',
        'category': 'entertainment',
        'tags': ['fortune', 'tarot', 'prediction', 'mysticism']
    },
    {
        'name': 'Coin Flip',
        'description': 'Simple random chance generator',
        'endpoint': 'coin_flip.index',
        'icon': '🪙',
        'category': 'entertainment',
        'tags': ['coin', 'flip', 'random', 'chance']
    },
    {
        'name': 'Prank Helper',
        'description': 'Cosmic mischief assistance tools',
        'endpoint': 'prank_helper.index',
        'icon': '😈',
        'category': 'entertainment',
        'tags': ['prank', 'mischief', 'jokes', 'tricks']
    },
    
    # Puzzles/Brain Games
    {
        'name': 'Guessing Game',
        'description': 'Test your psychic prediction powers',
        'endpoint': 'guessing_game.index',
        'icon': '🎯',
        'category': 'puzzle',
        'tags': ['guessing', 'numbers', 'prediction', 'logic']
    },
    {
        'name': 'Block Blast',
        'description': 'Tetris-style puzzle madness',
        'endpoint': 'block_blast.index',
        'icon': '🔳',
        'category': 'puzzle',
        'tags': ['tetris', 'blocks', 'puzzle', 'strategy']
    },
    {
        'name': 'Space Cargo Manager',
        'description': 'Organize cosmic deliveries with drag & drop',
        'endpoint': 'drag_drop.index',
        'icon': '📦',
        'category': 'puzzle',
        'tags': ['drag', 'drop', 'cargo', 'organization']
    },
    {
        'name': 'Wire Matching',
        'description': 'Connect the electrical circuits',
        'endpoint': 'wire_matching.index',
        'icon': '🔌',
        'category': 'puzzle',
        'tags': ['wires', 'circuits', 'electrical', 'matching']
    },
    {
        'name': 'Number Sequence',
        'description': 'Follow the mathematical patterns',
        'endpoint': 'number_sequence.index',
        'icon': '🔢',
        'category': 'puzzle',
        'tags': ['numbers', 'sequence', 'math', 'pattern']
    },
    {
        'name': 'Space Door Control',
        'description': 'Manage airlock security systems',
        'endpoint': 'door_game.index',
        'icon': '🚪',
        'category': 'puzzle',
        'tags': ['doors', 'airlock', 'security', 'control']
    },
    {
        'name': 'I Spy Game',
        'description': 'Find hidden cosmic objects',
        'endpoint': 'i_spy.index',
        'icon': '🔍',
        'category': 'puzzle',
        'tags': ['spy', 'find', 'hidden', 'search']
    },
    {
        'name': 'Connect Dots',
        'description': 'Link celestial connection points',
        'endpoint': 'connect_dots.index',
        'icon': '🔗',
        'category': 'puzzle',
        'tags': ['connect', 'dots', 'lines', 'pattern']
    },
    {
        'name': 'Balance Scale Game',
        'description': 'Master physics and equilibrium',
        'endpoint': 'balance_scale.index',
        'icon': '⚖️',
        'category': 'puzzle',
        'tags': ['balance', 'scale', 'physics', 'weight']
    },
    {
        'name': 'Lockpick Game',
        'description': 'Master the art of lock manipulation',
        'endpoint': 'lockpick_game.index',
        'icon': '🔓',
        'category': 'puzzle',
        'tags': ['lockpick', 'locks', 'security', 'skill']
    },
    {
        'name': '2048 - Space Edition',
        'description': 'Combine numbers in cosmic style',
        'endpoint': 'game_2048.index',
        'icon': '🎲',
        'category': 'puzzle',
        'tags': ['2048', 'numbers', 'combination', 'strategy']
    },
    {
        'name': 'Space Maze Navigator',
        'description': 'Navigate through cosmic labyrinths',
        'endpoint': 'maze_game.index',
        'icon': '🚀',
        'category': 'puzzle',
        'tags': ['maze', 'navigation', 'labyrinth', 'space']
    },
    
    # Word Games
    {
        'name': 'Hangman',
        'description': 'Word guessing in the dark void',
        'endpoint': 'hangman.index',
        'icon': '🔮',
        'category': 'word',
        'tags': ['hangman', 'words', 'guessing', 'vocabulary']
    },
    {
        'name': 'Space Wordle',
        'description': 'Word puzzles from distant worlds',
        'endpoint': 'wordle.index',
        'icon': '🔤',
        'category': 'word',
        'tags': ['wordle', 'words', 'puzzle', 'letters']
    },
    {
        'name': 'Story Generator',
        'description': 'Create galactic adventures with words',
        'endpoint': 'story_generator.index',
        'icon': '📖',
        'category': 'creative',
        'tags': ['story', 'creative', 'writing', 'adventure']
    },
    
    # Skill/Timing Games
    {
        'name': 'Time Predict Challenge',
        'description': 'Test your internal clock - hit exactly 10.000 seconds!',
        'endpoint': 'time_predict.index',
        'icon': '🕒',
        'category': 'skill',
        'tags': ['time', 'timing', 'predict', 'precision', '10 seconds', 'challenge']
    },
    {
        'name': 'Typing Test',
        'description': 'Measure your keyboard velocity',
        'endpoint': 'typing_test.index',
        'icon': '⌨️',
        'category': 'skill',
        'tags': ['typing', 'speed', 'keyboard', 'wpm']
    },
    {
        'name': 'Click Speed Calculator',
        'description': 'Test your clicking prowess',
        'endpoint': 'click_speed.index',
        'icon': '⚡',
        'category': 'skill',
        'tags': ['click', 'speed', 'fast', 'reaction']
    },
    {
        'name': 'Shell Game',
        'description': 'Follow the cosmic cup challenge',
        'endpoint': 'shell_game.index',
        'icon': '🎪',
        'category': 'skill',
        'tags': ['shell', 'follow', 'tracking', 'attention']
    },
    {
        'name': 'OSU! Clone',
        'description': 'Rhythm clicking mastery',
        'endpoint': 'osu_game.index',
        'icon': '🎯',
        'category': 'skill',
        'tags': ['osu', 'rhythm', 'clicking', 'music']
    },
    {
        'name': 'Bomb Defuser',
        'description': 'Disarm explosive devices under pressure',
        'endpoint': 'bomb_defuse.index',
        'icon': '💣',
        'category': 'skill',
        'tags': ['bomb', 'defuse', 'pressure', 'danger']
    },
    {
        'name': 'Slider Challenge',
        'description': 'Master precision control systems',
        'endpoint': 'slider_challenge.index',
        'icon': '🎚️',
        'category': 'skill',
        'tags': ['slider', 'precision', 'control', 'accuracy']
    },
    {
        'name': 'Speed Sort Challenge',
        'description': 'Sort items at lightning speed',
        'endpoint': 'speed_sort.index',
        'icon': '⚡',
        'category': 'skill',
        'tags': ['sort', 'speed', 'organize', 'fast']
    },
    {
        'name': 'One-Pixel Hunt',
        'description': 'Find the needle in the digital haystack',
        'endpoint': 'one_pixel_hunt.index',
        'icon': '🔍',
        'category': 'skill',
        'tags': ['pixel', 'hunt', 'precision', 'find']
    },
    
    # Arcade/Action Games
    {
        'name': 'Cosmic Dino Runner',
        'description': 'Chrome dinosaur game in space - jump over obstacles!',
        'endpoint': 'dino_runner.index',
        'icon': '🦕',
        'category': 'arcade',
        'tags': ['dino', 'runner', 'jumping', 'endless', 'chrome', 'obstacles', 'classic']
    },
    {
        'name': 'Snake Game',
        'description': 'Classic serpent navigation challenge',
        'endpoint': 'snake_game.index',
        'icon': '🐍',
        'category': 'arcade',
        'tags': ['snake', 'classic', 'navigation', 'grow']
    },
    {
        'name': 'Click Clear Game',
        'description': 'Clean up the cosmic debris field',
        'endpoint': 'click_clear.index',
        'icon': '💫',
        'category': 'arcade',
        'tags': ['click', 'clear', 'cleanup', 'debris']
    },
    {
        'name': 'Space Invaders',
        'description': 'Classic alien shooting action',
        'endpoint': 'space_invaders.index',
        'icon': '🛸',
        'category': 'arcade',
        'tags': ['space', 'invaders', 'shooting', 'aliens']
    },
    {
        'name': 'Brick Breaker Game',
        'description': 'Smash through cosmic barriers',
        'endpoint': 'brick_breaker.index',
        'icon': '🧱',
        'category': 'arcade',
        'tags': ['brick', 'breaker', 'ball', 'paddle']
    },
    {
        'name': 'Cosmic Pong',
        'description': 'Interstellar paddle battle',
        'endpoint': 'pong.index',
        'icon': '🏓',
        'category': 'arcade',
        'tags': ['pong', 'paddle', 'ball', 'classic']
    },
    {
        'name': 'Rage Slots',
        'description': 'High-intensity slot machine action',
        'endpoint': 'slots_machine.index',
        'icon': '🎰',
        'category': 'arcade',
        'tags': ['slots', 'machine', 'gambling', 'rage']
    },
    
    # Strategy Games
    {
        'name': 'Tic Tac Toe',
        'description': 'Strategic grid warfare',
        'endpoint': 'tic_tac_toe.index',
        'icon': '⚡',
        'category': 'strategy',
        'tags': ['tic', 'tac', 'toe', 'grid', 'strategy']
    },
    {
        'name': 'Rock Paper Scissors',
        'description': 'Ancient combat techniques',
        'endpoint': 'rock_paper_scissors.index',
        'icon': '⚔️',
        'category': 'strategy',
        'tags': ['rock', 'paper', 'scissors', 'battle']
    },
    {
        'name': 'Space Pattern Memory',
        'description': 'Remember complex stellar sequences',
        'endpoint': 'space_memory_game.index',
        'icon': '🎴',
        'category': 'strategy',
        'tags': ['memory', 'pattern', 'sequence', 'cards']
    },
    
    # Educational
    {
        'name': 'Mountain Academy',
        'description': 'Train your mathematical prowess',
        'endpoint': 'multiplication_trainer.index',
        'icon': '🏔️',
        'category': 'education',
        'tags': ['math', 'multiplication', 'training', 'academy']
    },
    {
        'name': 'Coordinate Hunter',
        'description': 'Navigate mathematical coordinate space',
        'endpoint': 'coordinate_game.index',
        'icon': '🎯',
        'category': 'education',
        'tags': ['coordinates', 'math', 'navigation', 'points']
    },
    
    # Health/Utility
    {
        'name': 'Water Tracker',
        'description': 'Monitor your hydration levels',
        'endpoint': 'water_drinker.index',
        'icon': '💧',
        'category': 'health',
        'tags': ['water', 'hydration', 'health', 'tracker']
    },
    
    # Simulation
    {
        'name': "Lucky's Temperature Control",
        'description': 'Regulate your pet tortoise habitat',
        'endpoint': 'tortoise_temp.index',
        'icon': '🐢',
        'category': 'simulation',
        'tags': ['tortoise', 'temperature', 'pet', 'control']
    },
]

# Categories for filtering (auto-generated from games data)
def get_categories():
    """Get all unique categories from games data"""
    categories = set()
    for game in GAMES_DATA:
        categories.add(game['category'])
    return sorted(list(categories))

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

# ===== ROUTES =====

@test_home.route('/')
def index():
    """
    Main test homepage route - displays scrollable game collection
    """
    categories = get_categories()
    
    # Get optional category filter from URL parameters
    selected_category = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    # Filter games based on parameters
    if search_query:
        games = search_games(search_query)
    else:
        games = get_games_by_category(selected_category if selected_category else None)
    
    return render_template('test_home.html',
                         games=games,
                         categories=categories,
                         selected_category=selected_category,
                         search_query=search_query,
                         total_games=len(GAMES_DATA))

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
    API endpoint to get all categories
    """
    return jsonify({
        'success': True,
        'categories': get_categories()
    })

@test_home.route('/stats')
def stats():
    """
    Show statistics about the game collection
    """
    categories = get_categories()
    stats_data = {
        'total_games': len(GAMES_DATA),
        'total_categories': len(categories),
        'category_breakdown': {}
    }
    
    # Count games per category
    for category in categories:
        games_in_category = len(get_games_by_category(category))
        stats_data['category_breakdown'][category] = games_in_category
    
    return jsonify({
        'success': True,
        'stats': stats_data
    })

# ===== HELPER FUNCTIONS FOR EASY MAINTENANCE =====

def add_game(name, description, endpoint, icon, category, tags):
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
        'tags': tags if isinstance(tags, list) else [tags]
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

# Run validation on import (for development)
if __name__ == '__main__':
    validate_game_data()