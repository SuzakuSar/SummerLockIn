from flask import Blueprint, render_template, request, jsonify, session
import time

# Create blueprint
fake_chatbot = Blueprint('fake_chatbot', __name__, template_folder='templates')

@fake_chatbot.route('/')
def index():
    """Main chatbot page - initialize chat session"""
    # Initialize chat state
    if 'chatbot_state' not in session:
        session['chatbot_state'] = 'initial'  # Track if we should say 'who' or 'asked'
        session['chatbot_messages'] = []
    
    return render_template('fake_chatbot.html')

@fake_chatbot.route('/api/chat', methods=['POST'])
def chat_api():
    """Handle chat messages and return bot response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Initialize session if needed
        if 'chatbot_state' not in session:
            session['chatbot_state'] = 'initial'
            session['chatbot_messages'] = []
        
        # Add user message to history
        session['chatbot_messages'].append({
            'type': 'user',
            'message': user_message,
            'timestamp': time.time()
        })
        
        # Determine bot response based on state
        if session['chatbot_state'] == 'initial':
            bot_response = "who"
            session['chatbot_state'] = 'asked_who'
        else:
            bot_response = "asked"
            session['chatbot_state'] = 'asked_who'  # Always go back to asking "who"
        
        # Add bot response to history
        session['chatbot_messages'].append({
            'type': 'bot',
            'message': bot_response,
            'timestamp': time.time()
        })
        
        # Keep only last 50 messages to prevent session bloat
        if len(session['chatbot_messages']) > 50:
            session['chatbot_messages'] = session['chatbot_messages'][-50:]
        
        # Save session
        session.modified = True
        
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fake_chatbot.route('/api/chat/reset', methods=['POST'])
def reset_chat():
    """Reset the chat conversation"""
    session['chatbot_state'] = 'initial'
    session['chatbot_messages'] = []
    session.modified = True
    
    return jsonify({
        'status': 'success',
        'message': 'Chat reset successfully'
    })

@fake_chatbot.route('/api/chat/history')
def get_chat_history():
    """Get chat message history"""
    messages = session.get('chatbot_messages', [])
    return jsonify({
        'messages': messages,
        'total_count': len(messages)
    })