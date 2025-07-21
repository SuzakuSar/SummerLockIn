# story_generator/story_generator.py
from flask import render_template, request, session, redirect, url_for, jsonify
from . import story_generator
from .story_templates import get_random_template, get_template_by_index, get_all_templates
import datetime

@story_generator.route('/')
def index():
    """Main story generator page - show template selection"""
    templates = get_all_templates()
    return render_template('story_form.html', templates=templates)

@story_generator.route('/create/<int:template_id>')
def create_story(template_id):
    """Show the word input form for a specific template"""
    template = get_template_by_index(template_id)
    return render_template('story_form.html', 
                         template=template, 
                         template_id=template_id,
                         show_form=True)

@story_generator.route('/generate', methods=['POST'])
def generate_story():
    """Generate a story from the submitted words"""
    template_id = request.form.get('template_id', type=int)
    template = get_template_by_index(template_id)
    
    # Collect all the words from the form
    story_words = {}
    for field in template['fields']:
        story_words[field] = request.form.get(field, '').strip()
    
    # Fill in the story template
    try:
        generated_story = template['template'].format(**story_words)
        story_title = template['title']
    except KeyError as e:
        return f"Error: Missing word for {e}", 400
    
    # Save to session history
    if 'story_generator_history' not in session:
        session['story_generator_history'] = []
    
    story_entry = {
        'title': story_title,
        'story': generated_story,
        'words': story_words,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'template_id': template_id
    }
    
    session['story_generator_history'].insert(0, story_entry)
    
    # Keep only the last 10 stories
    if len(session['story_generator_history']) > 10:
        session['story_generator_history'] = session['story_generator_history'][:10]
    
    session.modified = True
    
    return render_template('story_result.html', 
                         story_title=story_title,
                         story=generated_story,
                         words=story_words,
                         template_id=template_id)

@story_generator.route('/history')
def story_history():
    """Show user's story history"""
    history = session.get('story_generator_history', [])
    return render_template('story_history.html', stories=history)

@story_generator.route('/random')
def random_story():
    """Redirect to a random story template"""
    template = get_random_template()
    template_id = get_all_templates().index(template)
    return redirect(url_for('story_generator.create_story', template_id=template_id))

@story_generator.route('/clear-history')
def clear_history():
    """Clear the user's story history"""
    session.pop('story_generator_history', None)
    return redirect(url_for('story_generator.story_history'))

@story_generator.route('/api/word-suggestions/<word_type>')
def word_suggestions(word_type):
    """API endpoint for word suggestions (optional enhancement)"""
    suggestions = {
        'adjective': ['funny', 'sparkling', 'enormous', 'tiny', 'magical', 'grumpy', 'bouncy', 'slimy'],
        'noun': ['banana', 'robot', 'unicorn', 'pizza', 'dragon', 'telephone', 'spaceship', 'pickle'],
        'verb': ['dance', 'explode', 'whisper', 'juggle', 'teleport', 'giggle', 'swim', 'fly'],
        'animal': ['penguin', 'octopus', 'hamster', 'elephant', 'platypus', 'llama', 'kangaroo', 'turtle'],
        'adverb': ['quickly', 'mysteriously', 'loudly', 'gracefully', 'awkwardly', 'secretly', 'wildly', 'gently']
    }
    
    return jsonify(suggestions.get(word_type, []))