from flask import Blueprint, render_template, jsonify, session
import random
import time

typing_test = Blueprint('typing_test', __name__, template_folder='templates')

# Sample texts for typing test
SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog. This pangram contains every letter of the alphabet and is commonly used for typing practice.",
    "Programming is the art of telling another human being what one wants the computer to do. It requires patience, logic, and creativity.",
    "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole filled with the ends of worms and an oozy smell.",
    "Space exploration is the ultimate adventure. It represents our quest to understand the universe and our place within it.",
    "The internet has revolutionized how we communicate, learn, and share information across the globe in real time.",
    "Artificial intelligence and machine learning are transforming industries and creating new possibilities for human progress.",
    "Climate change represents one of the greatest challenges facing humanity in the twenty-first century and beyond.",
    "Books are the quietest and most constant of friends. They are the most accessible and wisest of counselors.",
]

@typing_test.route('/')
def index():
    """Main typing test page"""
    # Get random text for typing
    text_to_type = random.choice(SAMPLE_TEXTS)
    
    # Store in session for validation
    session['typing_test_text'] = text_to_type
    session['typing_test_start_time'] = None
    
    return render_template('typing_test.html', text_to_type=text_to_type)

@typing_test.route('/start', methods=['POST'])
def start_test():
    """Start the typing test timer"""
    session['typing_test_start_time'] = time.time()
    return jsonify({'status': 'started', 'timestamp': session['typing_test_start_time']})

@typing_test.route('/submit', methods=['POST'])
def submit_test():
    """Calculate and return typing test results"""
    from flask import request
    
    typed_text = request.json.get('typed_text', '')
    original_text = session.get('typing_test_text', '')
    start_time = session.get('typing_test_start_time')
    
    if not start_time:
        return jsonify({'error': 'Test not started'}), 400
    
    # Calculate time taken
    end_time = time.time()
    time_taken = end_time - start_time
    
    # Calculate words typed (assuming average word length of 5 characters)
    words_typed = len(typed_text) / 5
    
    # Calculate WPM
    wpm = round((words_typed / time_taken) * 60, 1) if time_taken > 0 else 0
    
    # Calculate accuracy
    correct_chars = 0
    total_chars = min(len(typed_text), len(original_text))
    
    for i in range(total_chars):
        if i < len(typed_text) and i < len(original_text):
            if typed_text[i] == original_text[i]:
                correct_chars += 1
    
    accuracy = round((correct_chars / total_chars) * 100, 1) if total_chars > 0 else 0
    
    # Store results in session
    session['typing_test_last_wpm'] = wpm
    session['typing_test_last_accuracy'] = accuracy
    session['typing_test_last_time'] = round(time_taken, 1)
    
    return jsonify({
        'wpm': wpm,
        'accuracy': accuracy,
        'time_taken': round(time_taken, 1),
        'total_chars': total_chars,
        'correct_chars': correct_chars
    })

@typing_test.route('/new-text')
def new_text():
    """Get a new random text for typing"""
    text_to_type = random.choice(SAMPLE_TEXTS)
    session['typing_test_text'] = text_to_type
    session['typing_test_start_time'] = None
    
    return jsonify({'text': text_to_type})