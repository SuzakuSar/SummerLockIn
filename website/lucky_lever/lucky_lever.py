# File: website/lucky_lever/lucky_lever.py
from flask import Blueprint, render_template, request, redirect, url_for
import random

# Create blueprint
lucky_lever = Blueprint('lucky_lever', __name__, template_folder='templates')

# Predefined fun search terms for random pulls
RANDOM_SEARCHES = [
    "cute animals",
    "amazing facts",
    "cool science experiments", 
    "funny memes",
    "beautiful places",
    "interesting history",
    "space facts",
    "ocean mysteries",
    "weird foods",
    "awesome inventions",
    "mind-blowing art",
    "random trivia",
    "cool photography",
    "unusual animals",
    "fun recipes",
    "amazing nature",
    "quirky websites",
    "fascinating documentaries",
    "random wikipedia",
    "surprise me"
]

@lucky_lever.route('/')
def index():
    """Main lucky lever page"""
    return render_template('lucky_lever.html')

@lucky_lever.route('/pull', methods=['POST'])
def pull_lever():
    """Handle lever pull and redirect to Google I'm Feeling Lucky"""
    search_term = request.form.get('search_term', '').strip()
    
    # If no search term provided, use a random one
    if not search_term:
        search_term = random.choice(RANDOM_SEARCHES)
    
    # Google I'm Feeling Lucky URL
    google_lucky_url = f"https://www.google.com/search?q={search_term}&btnI=1"
    
    return redirect(google_lucky_url)

@lucky_lever.route('/api/random-search')
def get_random_search():
    """API endpoint to get a random search term"""
    return {'search_term': random.choice(RANDOM_SEARCHES)}