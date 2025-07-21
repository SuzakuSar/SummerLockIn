# File: website/drag_drop/drag_drop.py
from flask import Blueprint, render_template, request, session, jsonify
import random

drag_drop = Blueprint('drag_drop', __name__, template_folder='templates')

# Space cargo items with different sizes and values
CARGO_ITEMS = [
    {'id': 'crystal', 'name': 'Energy Crystal', 'size': 2, 'value': 50, 'emoji': '💎'},
    {'id': 'artifact', 'name': 'Ancient Artifact', 'size': 3, 'value': 75, 'emoji': '🏺'},
    {'id': 'ore', 'name': 'Cosmic Ore', 'size': 1, 'value': 25, 'emoji': '⚱️'},
    {'id': 'device', 'name': 'Tech Device', 'size': 2, 'value': 40, 'emoji': '📱'},
    {'id': 'relic', 'name': 'Space Relic', 'size': 4, 'value': 100, 'emoji': '🔮'},
    {'id': 'fuel', 'name': 'Fuel Cell', 'size': 2, 'value': 30, 'emoji': '🔋'},
    {'id': 'data', 'name': 'Data Core', 'size': 1, 'value': 35, 'emoji': '💾'},
    {'id': 'weapon', 'name': 'Plasma Weapon', 'size': 3, 'value': 80, 'emoji': '🔫'},
]

MAX_CARGO_CAPACITY = 15  # Total size units the cargo bay can hold

@drag_drop.route('/')
def index():
    """Main drag and drop game page"""
    # Initialize session data if not exists
    if 'drag_drop_cargo' not in session:
        session['drag_drop_cargo'] = []
        session['drag_drop_score'] = 0
        session['drag_drop_available_items'] = generate_available_items()
    
    cargo_items = session.get('drag_drop_cargo', [])
    current_capacity = sum(item['size'] for item in cargo_items)
    available_items = session.get('drag_drop_available_items', [])
    
    return render_template('drag_drop.html.jinja2',
                         cargo_items=cargo_items,
                         available_items=available_items,
                         current_capacity=current_capacity,
                         max_capacity=MAX_CARGO_CAPACITY,
                         score=session.get('drag_drop_score', 0),
                         is_full=current_capacity >= MAX_CARGO_CAPACITY)

@drag_drop.route('/add_item', methods=['POST'])
def add_item():
    """Add an item to the cargo bay"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    # Find the item in available items
    available_items = session.get('drag_drop_available_items', [])
    item_to_add = None
    
    for item in available_items:
        if item['id'] == item_id:
            item_to_add = item
            break
    
    if not item_to_add:
        return jsonify({'success': False, 'message': 'Item not found'})
    
    # Check if there's space in cargo
    cargo_items = session.get('drag_drop_cargo', [])
    current_capacity = sum(item['size'] for item in cargo_items)
    
    if current_capacity + item_to_add['size'] > MAX_CARGO_CAPACITY:
        return jsonify({'success': False, 'message': 'Not enough space in cargo bay!'})
    
    # Add item to cargo and remove from available
    cargo_items.append(item_to_add)
    available_items.remove(item_to_add)
    
    # Update score and session
    session['drag_drop_cargo'] = cargo_items
    session['drag_drop_available_items'] = available_items
    session['drag_drop_score'] = session.get('drag_drop_score', 0) + item_to_add['value']
    
    new_capacity = current_capacity + item_to_add['size']
    
    return jsonify({
        'success': True,
        'new_capacity': new_capacity,
        'score': session['drag_drop_score'],
        'is_full': new_capacity >= MAX_CARGO_CAPACITY,
        'message': f'Added {item_to_add["name"]} to cargo bay!'
    })

@drag_drop.route('/remove_item', methods=['POST'])
def remove_item():
    """Remove an item from the cargo bay"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    cargo_items = session.get('drag_drop_cargo', [])
    available_items = session.get('drag_drop_available_items', [])
    
    # Find and remove item from cargo
    item_to_remove = None
    for i, item in enumerate(cargo_items):
        if item['id'] == item_id:
            item_to_remove = cargo_items.pop(i)
            break
    
    if not item_to_remove:
        return jsonify({'success': False, 'message': 'Item not found in cargo'})
    
    # Add back to available items and update session
    available_items.append(item_to_remove)
    session['drag_drop_cargo'] = cargo_items
    session['drag_drop_available_items'] = available_items
    session['drag_drop_score'] = max(0, session.get('drag_drop_score', 0) - item_to_remove['value'])
    
    new_capacity = sum(item['size'] for item in cargo_items)
    
    return jsonify({
        'success': True,
        'new_capacity': new_capacity,
        'score': session['drag_drop_score'],
        'is_full': False,
        'message': f'Removed {item_to_remove["name"]} from cargo bay!'
    })

@drag_drop.route('/reset')
def reset_game():
    """Reset the game state"""
    session.pop('drag_drop_cargo', None)
    session.pop('drag_drop_score', None)
    session.pop('drag_drop_available_items', None)
    return jsonify({'success': True, 'message': 'Game reset!'})

@drag_drop.route('/new_items')
def new_items():
    """Generate new available items"""
    session['drag_drop_available_items'] = generate_available_items()
    return jsonify({'success': True, 'message': 'New items generated!'})

def generate_available_items():
    """Generate a random selection of available items"""
    items = []
    num_items = random.randint(6, 10)
    
    for _ in range(num_items):
        base_item = random.choice(CARGO_ITEMS)
        # Create unique item with random ID
        item = base_item.copy()
        item['id'] = f"{base_item['id']}_{random.randint(1000, 9999)}"
        items.append(item)
    
    return items