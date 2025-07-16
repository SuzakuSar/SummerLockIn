"""
Mountain Academy - Multiplication Trainer Blueprint
A mountain climbing themed multiplication facts practice app with extensive customization
and quality of life features for the SUMMERLOCKIN project.
"""

from flask import Blueprint, render_template, request, session, jsonify
import random
import time
from datetime import datetime, timedelta

# Create blueprint with template folder specification
multiplication_trainer = Blueprint('multiplication_trainer', __name__, template_folder='templates')

# Constants for the mountain academy system
CLIMBING_RANKS = [
    {'name': 'Base Camp Visitor', 'min_elevation': 0, 'icon': '🥾'},
    {'name': 'Trail Walker', 'min_elevation': 100, 'icon': '🚶'},
    {'name': 'Hill Climber', 'min_elevation': 250, 'icon': '⛰️'},
    {'name': 'Mountain Hiker', 'min_elevation': 500, 'icon': '🏔️'},
    {'name': 'Peak Challenger', 'min_elevation': 1000, 'icon': '🗻'},
    {'name': 'Summit Master', 'min_elevation': 2000, 'icon': '🏆'},
    {'name': 'Everest Legend', 'min_elevation': 5000, 'icon': '👑'}
]

TRAIL_BADGES = [
    {'id': 'first_steps', 'name': 'First Steps', 'desc': 'Complete your first climbing expedition', 'icon': '👣'},
    {'id': 'swift_climber', 'name': 'Swift Climber', 'desc': 'Answer 10 questions in under 30 seconds', 'icon': '💨'},
    {'id': 'perfect_path', 'name': 'Perfect Path', 'desc': 'Get 20 questions correct in a row', 'icon': '✨'},
    {'id': 'trail_master', 'name': 'Trail Master', 'desc': 'Master all multiplication tables 1-12', 'icon': '🎒'},
    {'id': 'endurance_hiker', 'name': 'Endurance Hiker', 'desc': 'Complete a 100-question expedition', 'icon': '💪'},
    {'id': 'daily_climber', 'name': 'Daily Climber', 'desc': 'Practice 5 days in a row', 'icon': '📅'}
]

def init_session():
    """Initialize session variables for the multiplication trainer"""
    prefix = 'mult_trainer_'
    
    # User progress tracking
    if f'{prefix}total_elevation' not in session:
        session[f'{prefix}total_elevation'] = 0
    if f'{prefix}total_questions' not in session:
        session[f'{prefix}total_questions'] = 0
    if f'{prefix}total_correct' not in session:
        session[f'{prefix}total_correct'] = 0
    if f'{prefix}earned_badges' not in session:
        session[f'{prefix}earned_badges'] = []
    if f'{prefix}practice_streak' not in session:
        session[f'{prefix}practice_streak'] = 0
    if f'{prefix}last_practice_date' not in session:
        session[f'{prefix}last_practice_date'] = None
    if f'{prefix}table_mastery' not in session:
        session[f'{prefix}table_mastery'] = {str(i): False for i in range(1, 13)}
    
    # Current expedition settings
    if f'{prefix}current_settings' not in session:
        session[f'{prefix}current_settings'] = {
            'tables': [2, 3, 4, 5],  # Default tables to practice
            'question_count': 20,
            'time_limit': None,  # None for unlimited time
            'difficulty': 'mixed',  # 'easy', 'medium', 'hard', 'mixed'
            'show_hints': True,
            'play_sounds': True
        }
    
    # Current expedition state
    if f'{prefix}current_expedition' not in session:
        session[f'{prefix}current_expedition'] = None

def get_current_rank():
    """Get the user's current climbing rank based on total elevation"""
    total_elevation = session.get('mult_trainer_total_elevation', 0)
    current_rank = CLIMBING_RANKS[0]
    
    for rank in CLIMBING_RANKS:
        if total_elevation >= rank['min_elevation']:
            current_rank = rank
        else:
            break
    
    return current_rank

def get_next_rank():
    """Get the next rank the user can achieve"""
    total_elevation = session.get('mult_trainer_total_elevation', 0)
    
    for rank in CLIMBING_RANKS:
        if total_elevation < rank['min_elevation']:
            return rank
    
    return None  # User has achieved the highest rank

def check_new_badges(expedition_stats):
    """Check if user earned any new badges from this expedition"""
    prefix = 'mult_trainer_'
    earned_badges = session.get(f'{prefix}earned_badges', [])
    new_badges = []
    
    # First Steps badge
    if 'first_steps' not in earned_badges:
        new_badges.append('first_steps')
    
    # Swift Climber badge
    if ('swift_climber' not in earned_badges and 
        expedition_stats.get('questions_answered', 0) >= 10 and
        expedition_stats.get('total_time', float('inf')) <= 30):
        new_badges.append('swift_climber')
    
    # Perfect Path badge
    if ('perfect_path' not in earned_badges and 
        expedition_stats.get('max_streak', 0) >= 20):
        new_badges.append('perfect_path')
    
    # Endurance Hiker badge
    if ('endurance_hiker' not in earned_badges and 
        expedition_stats.get('questions_answered', 0) >= 100):
        new_badges.append('endurance_hiker')
    
    # Daily Climber badge (check practice streak)
    if ('daily_climber' not in earned_badges and 
        session.get(f'{prefix}practice_streak', 0) >= 5):
        new_badges.append('daily_climber')
    
    # Trail Master badge (check table mastery)
    table_mastery = session.get(f'{prefix}table_mastery', {})
    if ('trail_master' not in earned_badges and 
        all(table_mastery.values())):
        new_badges.append('trail_master')
    
    # Add new badges to session
    session[f'{prefix}earned_badges'] = earned_badges + new_badges
    
    return new_badges

def update_practice_streak():
    """Update the user's practice streak"""
    prefix = 'mult_trainer_'
    today = datetime.now().date()
    last_date_str = session.get(f'{prefix}last_practice_date')
    
    if last_date_str:
        last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
        days_diff = (today - last_date).days
        
        if days_diff == 1:
            # Consecutive day - increment streak
            session[f'{prefix}practice_streak'] = session.get(f'{prefix}practice_streak', 0) + 1
        elif days_diff > 1:
            # Broke streak - reset to 1
            session[f'{prefix}practice_streak'] = 1
        # If days_diff == 0, user already practiced today, don't change streak
    else:
        # First time practicing
        session[f'{prefix}practice_streak'] = 1
    
    session[f'{prefix}last_practice_date'] = today.strftime('%Y-%m-%d')

@multiplication_trainer.route('/')
def index():
    """Main page for the Mountain Academy multiplication trainer"""
    init_session()
    
    current_rank = get_current_rank()
    next_rank = get_next_rank()
    earned_badges = session.get('mult_trainer_earned_badges', [])
    
    # Get badge objects for earned badges
    user_badges = [badge for badge in TRAIL_BADGES if badge['id'] in earned_badges]
    
    # Calculate progress to next rank
    progress_to_next = 0
    if next_rank:
        current_elevation = session.get('mult_trainer_total_elevation', 0)
        elevation_needed = next_rank['min_elevation'] - current_elevation
        prev_rank_elevation = current_rank['min_elevation']
        progress_range = next_rank['min_elevation'] - prev_rank_elevation
        progress_to_next = max(0, min(100, ((current_elevation - prev_rank_elevation) / progress_range) * 100))
    
    stats = {
        'total_elevation': session.get('mult_trainer_total_elevation', 0),
        'total_questions': session.get('mult_trainer_total_questions', 0),
        'total_correct': session.get('mult_trainer_total_correct', 0),
        'accuracy': (session.get('mult_trainer_total_correct', 0) / max(1, session.get('mult_trainer_total_questions', 1))) * 100,
        'practice_streak': session.get('mult_trainer_practice_streak', 0),
        'badges_earned': len(earned_badges),
        'tables_mastered': sum(1 for mastered in session.get('mult_trainer_table_mastery', {}).values() if mastered)
    }
    
    return render_template('mountain_academy.html.jinja2',
                         current_rank=current_rank,
                         next_rank=next_rank,
                         progress_to_next=progress_to_next,
                         user_badges=user_badges,
                         all_badges=TRAIL_BADGES,
                         stats=stats)

@multiplication_trainer.route('/expedition-setup')
def expedition_setup():
    """Page for customizing expedition settings"""
    init_session()
    current_settings = session.get('mult_trainer_current_settings', {})
    
    return render_template('expedition_setup.html.jinja2', settings=current_settings)

@multiplication_trainer.route('/start-expedition', methods=['POST'])
def start_expedition():
    """Start a new multiplication practice expedition"""
    init_session()
    
    # Get settings from form
    settings = {
        'tables': [int(x) for x in request.form.getlist('tables')],
        'question_count': int(request.form.get('question_count', 20)),
        'time_limit': int(request.form.get('time_limit')) if request.form.get('time_limit') else None,
        'difficulty': request.form.get('difficulty', 'mixed'),
        'show_hints': 'show_hints' in request.form,
        'play_sounds': 'play_sounds' in request.form
    }
    
    # Validate settings
    if not settings['tables']:
        settings['tables'] = [2, 3, 4, 5]  # Default if none selected
    
    settings['question_count'] = max(5, min(200, settings['question_count']))  # Limit range
    
    # Save settings
    session['mult_trainer_current_settings'] = settings
    
    # Initialize expedition
    expedition = {
        'settings': settings,
        'questions': generate_questions(settings),
        'current_question': 0,
        'correct_answers': 0,
        'incorrect_answers': 0,
        'start_time': time.time(),
        'question_start_time': time.time(),
        'answer_times': [],
        'streak': 0,
        'max_streak': 0,
        'completed': False
    }
    
    session['mult_trainer_current_expedition'] = expedition
    
    return render_template('expedition_practice.html.jinja2', expedition=expedition)

def generate_questions(settings):
    """Generate multiplication questions based on settings"""
    questions = []
    tables = settings['tables']
    question_count = settings['question_count']
    difficulty = settings['difficulty']
    
    for _ in range(question_count):
        # Select random table
        table = random.choice(tables)
        
        # Select multiplier based on difficulty
        if difficulty == 'easy':
            multiplier = random.randint(1, 5)
        elif difficulty == 'medium':
            multiplier = random.randint(6, 10)
        elif difficulty == 'hard':
            multiplier = random.randint(11, 15)
        else:  # mixed
            multiplier = random.randint(1, 12)
        
        # Randomly swap operands for variety
        if random.random() < 0.5:
            num1, num2 = table, multiplier
        else:
            num1, num2 = multiplier, table
        
        answer = num1 * num2
        
        # Generate wrong answer choices for multiple choice
        wrong_answers = []
        while len(wrong_answers) < 3:
            # Generate plausible wrong answers
            if random.random() < 0.3:
                # Off by one in factors
                wrong = (num1 + random.choice([-1, 1])) * num2
            elif random.random() < 0.3:
                wrong = num1 * (num2 + random.choice([-1, 1]))
            else:
                # Random nearby number
                wrong = answer + random.randint(-10, 10)
            
            if wrong > 0 and wrong != answer and wrong not in wrong_answers:
                wrong_answers.append(wrong)
        
        # Create choices list and shuffle
        choices = [answer] + wrong_answers
        random.shuffle(choices)
        
        questions.append({
            'num1': num1,
            'num2': num2,
            'answer': answer,
            'choices': choices,
            'table': min(num1, num2)  # Track which table this tests
        })
    
    return questions

@multiplication_trainer.route('/submit-answer', methods=['POST'])
def submit_answer():
    """Handle answer submission during expedition"""
    init_session()
    
    expedition = session.get('mult_trainer_current_expedition')
    if not expedition or expedition['completed']:
        return jsonify({'error': 'No active expedition'})
    
    answer = int(request.form.get('answer'))
    current_q = expedition['current_question']
    question = expedition['questions'][current_q]
    correct = answer == question['answer']
    
    # Record timing
    question_time = time.time() - expedition['question_start_time']
    expedition['answer_times'].append(question_time)
    
    # Update stats
    if correct:
        expedition['correct_answers'] += 1
        expedition['streak'] += 1
        expedition['max_streak'] = max(expedition['max_streak'], expedition['streak'])
    else:
        expedition['incorrect_answers'] += 1
        expedition['streak'] = 0
    
    # Move to next question
    expedition['current_question'] += 1
    expedition['question_start_time'] = time.time()
    
    # Check if expedition is complete
    if expedition['current_question'] >= len(expedition['questions']):
        expedition['completed'] = True
        expedition['end_time'] = time.time()
        
        # Process expedition completion
        return complete_expedition(expedition)
    
    session['mult_trainer_current_expedition'] = expedition
    
    return jsonify({
        'correct': correct,
        'correct_answer': question['answer'],
        'completed': False,
        'progress': {
            'current': expedition['current_question'],
            'total': len(expedition['questions']),
            'correct': expedition['correct_answers'],
            'streak': expedition['streak']
        }
    })

def complete_expedition(expedition):
    """Process completed expedition and update user progress"""
    prefix = 'mult_trainer_'
    
    # Calculate stats
    total_time = expedition['end_time'] - expedition['start_time']
    accuracy = (expedition['correct_answers'] / len(expedition['questions'])) * 100
    avg_time = sum(expedition['answer_times']) / len(expedition['answer_times'])
    
    # Calculate elevation gained (points)
    base_elevation = expedition['correct_answers'] * 5
    time_bonus = max(0, 50 - avg_time) * 2 if avg_time < 10 else 0
    accuracy_bonus = (accuracy - 50) * 2 if accuracy > 50 else 0
    streak_bonus = expedition['max_streak'] * 3
    
    elevation_gained = int(base_elevation + time_bonus + accuracy_bonus + streak_bonus)
    
    # Update global stats
    session[f'{prefix}total_elevation'] = session.get(f'{prefix}total_elevation', 0) + elevation_gained
    session[f'{prefix}total_questions'] = session.get(f'{prefix}total_questions', 0) + len(expedition['questions'])
    session[f'{prefix}total_correct'] = session.get(f'{prefix}total_correct', 0) + expedition['correct_answers']
    
    # Update table mastery
    table_mastery = session.get(f'{prefix}table_mastery', {})
    for question in expedition['questions']:
        table = str(question['table'])
        if table in table_mastery:
            # Mark as mastered if got most questions right for this table
            table_questions = [q for q in expedition['questions'] if str(q['table']) == table]
            table_correct = sum(1 for i, q in enumerate(expedition['questions']) 
                              if str(q['table']) == table and i < expedition['current_question'] 
                              and expedition['answer_times'][i] is not None)
            if len(table_questions) >= 3 and (table_correct / len(table_questions)) >= 0.8:
                table_mastery[table] = True
    
    session[f'{prefix}table_mastery'] = table_mastery
    
    # Update practice streak
    update_practice_streak()
    
    # Check for new badges
    expedition_stats = {
        'questions_answered': len(expedition['questions']),
        'total_time': total_time,
        'max_streak': expedition['max_streak'],
        'accuracy': accuracy
    }
    
    new_badges = check_new_badges(expedition_stats)
    
    # Prepare results
    results = {
        'questions_answered': len(expedition['questions']),
        'correct_answers': expedition['correct_answers'],
        'accuracy': accuracy,
        'total_time': total_time,
        'avg_time_per_question': avg_time,
        'max_streak': expedition['max_streak'],
        'elevation_gained': elevation_gained,
        'new_badges': new_badges,
        'current_rank': get_current_rank(),
        'next_rank': get_next_rank()
    }
    
    # Clear current expedition
    session[f'{prefix}current_expedition'] = None
    
    return jsonify({
        'completed': True,
        'results': results
    })

@multiplication_trainer.route('/expedition-results')
def expedition_results():
    """Show results page after completing expedition"""
    # This would show detailed results, but for AJAX we return JSON above
    return render_template('expedition_results.html.jinja2')

@multiplication_trainer.route('/leaderboard')
def leaderboard():
    """Show leaderboard/progress tracking page"""
    init_session()
    
    # In a real app, this would pull from a database
    # For now, just show current user stats
    total_questions = session.get('mult_trainer_total_questions', 0)
    total_correct = session.get('mult_trainer_total_correct', 0)
    
    # Calculate accuracy safely (avoid division by zero)
    accuracy = (total_correct / max(1, total_questions)) * 100 if total_questions > 0 else 0
    
    stats = {
        'total_elevation': session.get('mult_trainer_total_elevation', 0),
        'total_questions': total_questions,
        'total_correct': total_correct,
        'accuracy': accuracy,  # Pre-calculated accuracy
        'practice_streak': session.get('mult_trainer_practice_streak', 0),
        'badges_earned': len(session.get('mult_trainer_earned_badges', [])),
    }
    
    return render_template('leaderboard.html.jinja2', stats=stats)

@multiplication_trainer.route('/api/stats')
def api_stats():
    """API endpoint for getting current user stats"""
    init_session()
    
    return jsonify({
        'total_elevation': session.get('mult_trainer_total_elevation', 0),
        'total_questions': session.get('mult_trainer_total_questions', 0),
        'total_correct': session.get('mult_trainer_total_correct', 0),
        'current_rank': get_current_rank(),
        'next_rank': get_next_rank(),
        'badges': session.get('mult_trainer_earned_badges', []),
        'streak': session.get('mult_trainer_practice_streak', 0)
    })

@multiplication_trainer.route('/test-buttons')
def test_buttons():
    """Temporary test page for debugging button issues"""
    init_session()
    
    # Create fake expedition data for testing
    test_expedition = {
        'questions': [
            {'num1': 3, 'num2': 5, 'answer': 15, 'choices': [10, 15, 20, 25]},
            {'num1': 4, 'num2': 6, 'answer': 24, 'choices': [20, 24, 28, 32]}
        ],
        'settings': {
            'show_hints': True,
            'play_sounds': True,
            'auto_advance': True
        }
    }
    
    return render_template('test_buttons.html.jinja2', expedition=test_expedition)