# File: website/tortoise_temp/tortoise_temp.py
from flask import Blueprint, render_template, session, jsonify, request
import random
import time

tortoise_temp = Blueprint('tortoise_temp', __name__, template_folder='templates')

# Tortoise temperature constants
HEALTHY_MIN = 75  # Minimum healthy temperature (°F)
HEALTHY_MAX = 85  # Maximum healthy temperature (°F)
TEMP_CHANGE_RATE = 0.5  # How much temp can change per second
FAN_POWER = 2.0  # How much fan cools per click
HEATER_POWER = 2.0  # How much heater warms per click

def initialize_game():
    """Initialize a new game session"""
    session['tortoise_current_temp'] = random.uniform(HEALTHY_MIN, HEALTHY_MAX)
    session['tortoise_score'] = 0
    session['tortoise_game_active'] = True
    session['tortoise_last_update'] = time.time()
    session['tortoise_health_time'] = 0  # Time spent in healthy range
    session['tortoise_warnings'] = 0  # Number of temperature warnings

def get_temperature_status(temp):
    """Get the status of the temperature"""
    if temp < HEALTHY_MIN - 5:
        return "critically_cold"
    elif temp < HEALTHY_MIN:
        return "cold"
    elif temp > HEALTHY_MAX + 5:
        return "critically_hot"
    elif temp > HEALTHY_MAX:
        return "hot"
    else:
        return "healthy"

def update_temperature():
    """Update temperature based on time passed and add random fluctuation"""
    if 'tortoise_last_update' not in session:
        session['tortoise_last_update'] = time.time()
        return
    
    current_time = time.time()
    time_diff = current_time - session['tortoise_last_update']
    
    # Random temperature change (tortoise's natural regulation)
    random_change = random.uniform(-TEMP_CHANGE_RATE, TEMP_CHANGE_RATE) * time_diff
    
    # Apply environmental factors (room tends toward 70°F)
    room_temp = 70
    current_temp = session.get('tortoise_current_temp', 80)
    environmental_drift = (room_temp - current_temp) * 0.1 * time_diff
    
    # Update temperature
    new_temp = current_temp + random_change + environmental_drift
    session['tortoise_current_temp'] = max(50, min(100, new_temp))  # Clamp between 50-100°F
    session['tortoise_last_update'] = current_time
    
    # Update health time if in healthy range
    if HEALTHY_MIN <= session['tortoise_current_temp'] <= HEALTHY_MAX:
        session['tortoise_health_time'] = session.get('tortoise_health_time', 0) + time_diff
        session['tortoise_score'] = int(session['tortoise_health_time'])

@tortoise_temp.route('/')
def index():
    """Main tortoise temperature game page"""
    # Initialize game if not exists
    if 'tortoise_current_temp' not in session:
        initialize_game()
    
    # Update temperature
    update_temperature()
    
    current_temp = session['tortoise_current_temp']
    status = get_temperature_status(current_temp)
    
    return render_template('tortoise_temp.html.jinja2', 
                         current_temp=round(current_temp, 1),
                         status=status,
                         score=session.get('tortoise_score', 0),
                         health_time=session.get('tortoise_health_time', 0),
                         healthy_min=HEALTHY_MIN,
                         healthy_max=HEALTHY_MAX)

@tortoise_temp.route('/api/temperature')
def get_temperature():
    """API endpoint to get current temperature"""
    update_temperature()
    
    current_temp = session['tortoise_current_temp']
    status = get_temperature_status(current_temp)
    
    return jsonify({
        'temperature': round(current_temp, 1),
        'status': status,
        'score': session.get('tortoise_score', 0),
        'health_time': round(session.get('tortoise_health_time', 0), 1),
        'is_healthy': HEALTHY_MIN <= current_temp <= HEALTHY_MAX
    })

@tortoise_temp.route('/api/use_fan', methods=['POST'])
def use_fan():
    """Use the fan to cool Lucky down"""
    update_temperature()
    
    # Apply fan cooling
    session['tortoise_current_temp'] -= FAN_POWER
    session['tortoise_current_temp'] = max(50, session['tortoise_current_temp'])  # Don't go below 50°F
    
    current_temp = session['tortoise_current_temp']
    status = get_temperature_status(current_temp)
    
    return jsonify({
        'temperature': round(current_temp, 1),
        'status': status,
        'score': session.get('tortoise_score', 0),
        'action': 'fan_used'
    })

@tortoise_temp.route('/api/use_heater', methods=['POST'])
def use_heater():
    """Use the heater to warm Lucky up"""
    update_temperature()
    
    # Apply heater warming
    session['tortoise_current_temp'] += HEATER_POWER
    session['tortoise_current_temp'] = min(100, session['tortoise_current_temp'])  # Don't go above 100°F
    
    current_temp = session['tortoise_current_temp']
    status = get_temperature_status(current_temp)
    
    return jsonify({
        'temperature': round(current_temp, 1),
        'status': status,
        'score': session.get('tortoise_score', 0),
        'action': 'heater_used'
    })

@tortoise_temp.route('/api/reset')
def reset_game():
    """Reset the game to start over"""
    initialize_game()
    return jsonify({'message': 'Game reset successfully'})