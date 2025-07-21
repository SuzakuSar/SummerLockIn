# website/fake_download/fake_download.py
from flask import Blueprint, render_template, jsonify, session
import random
import time

fake_download = Blueprint('fake_download', __name__, template_folder='templates')

# List of fake classified files
CLASSIFIED_FILES = [
    "PROJECT_STARGATE_PROTOCOLS.pdf",
    "AREA_51_PERSONNEL_RECORDS.xlsx", 
    "UFO_INCIDENT_REPORTS_1947-2023.zip",
    "CLASSIFIED_ALIEN_AUTOPSY_DATA.mp4",
    "TOP_SECRET_MOON_LANDING_FOOTAGE.avi",
    "GOVERNMENT_MIND_CONTROL_EXPERIMENTS.docx",
    "BIGFOOT_SURVEILLANCE_PHOTOS.rar",
    "ATLANTIS_DISCOVERY_COORDINATES.kml",
    "TIME_TRAVEL_RESEARCH_NOTES.txt",
    "ILLUMINATI_MEMBER_DATABASE.db",
    "ELVIS_WITNESS_PROTECTION_FILES.pdf",
    "FLAT_EARTH_EVIDENCE_ARCHIVE.7z",
    "ANTARCTICA_SECRET_BASE_BLUEPRINTS.dwg",
    "DINOSAUR_CLONING_PROTOCOLS.pdf",
    "SIMULATION_THEORY_PROOF.json"
]

@fake_download.route('/')
def index():
    """Main fake download page"""
    # Reset session data for fresh start
    session.pop('fake_download_progress', None)
    session.pop('fake_download_file', None)
    session.pop('fake_download_started', None)
    
    return render_template('fake_download.html')

@fake_download.route('/start_download')
def start_download():
    """Start a fake download process"""
    # Pick a random file
    selected_file = random.choice(CLASSIFIED_FILES)
    
    # Store in session
    session['fake_download_file'] = selected_file
    session['fake_download_progress'] = 0
    session['fake_download_started'] = True
    session['fake_download_speed'] = random.randint(50, 200)  # KB/s
    session['fake_download_size'] = random.randint(50, 500)   # MB
    
    return jsonify({
        'success': True,
        'filename': selected_file,
        'size_mb': session['fake_download_size'],
        'speed_kbs': session['fake_download_speed']
    })

@fake_download.route('/download_progress')
def download_progress():
    """Get current download progress"""
    if not session.get('fake_download_started'):
        return jsonify({'error': 'No download in progress'})
    
    current_progress = session.get('fake_download_progress', 0)
    
    # Simulate progress - go up by random amount but never past 94%
    if current_progress < 94:
        # Normal progress increment
        increment = random.randint(1, 8)
        new_progress = min(current_progress + increment, 94)
        session['fake_download_progress'] = new_progress
    else:
        # Stuck at 94%!
        new_progress = 94
    
    # Calculate fake transfer stats
    speed = session.get('fake_download_speed', 100)
    size_mb = session.get('fake_download_size', 100)
    downloaded_mb = (new_progress / 100) * size_mb
    remaining_mb = size_mb - downloaded_mb
    
    # Add some random status messages
    status_messages = [
        "Decrypting classified data...",
        "Bypassing government firewalls...",
        "Authenticating security clearance...",
        "Scanning for surveillance...",
        "Establishing secure connection...",
        "Downloading from Area 51 servers...",
        "Extracting top secret files...",
        "Verifying alien signatures...",
        "Processing classified intel...",
        "Almost there... just kidding, still stuck at 94%!"
    ]
    
    status = random.choice(status_messages) if new_progress < 94 else "ERROR: Download stuck at 94% - Government intervention detected!"
    
    return jsonify({
        'progress': new_progress,
        'speed_kbs': speed + random.randint(-20, 20),  # Fluctuating speed
        'downloaded_mb': round(downloaded_mb, 1),
        'total_mb': size_mb,
        'remaining_mb': round(remaining_mb, 1),
        'status': status,
        'stuck': new_progress >= 94
    })

@fake_download.route('/cancel_download')
def cancel_download():
    """Cancel the current download"""
    session.pop('fake_download_progress', None)
    session.pop('fake_download_file', None)
    session.pop('fake_download_started', None)
    session.pop('fake_download_speed', None)
    session.pop('fake_download_size', None)
    
    return jsonify({'success': True, 'message': 'Download cancelled - Your location has not been traced... yet.'})