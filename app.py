# app.py

from flask import Flask, render_template, request, jsonify
from triage_questions import TRIAGE_FLOW
import uuid

# Initialize the Flask application
app = Flask(__name__)

# A dictionary to store the state of each user's conversation
# In a real app, you'd use a database (e.g., Redis, PostgreSQL) for this.
user_sessions = {}

@app.route('/')
def index():
    """Renders the main chat page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles the chat logic."""
    data = request.json
    user_id = data.get("user_id")
    user_message = data.get("message", "").strip()

    # If no user_id, create a new session
    if not user_id:
        user_id = str(uuid.uuid4())
        user_sessions[user_id] = {
            'current_question_id': 'start',
            'answers': {}
        }
        current_question_id = 'start'
    else:
        session = user_sessions.get(user_id)
        if not session:
            # Handle error case where user_id is invalid
            return jsonify({"error": "Invalid session"}), 400

        # --- Determine the next question ---
        prev_question_id = session['current_question_id']
        prev_question_node = TRIAGE_FLOW[prev_question_id]
        
        # Save the user's last answer
        session['answers'][prev_question_id] = user_message

        # Find the next question based on logic
        if prev_question_node['type'] == 'open-text':
            current_question_id = prev_question_node['next_question_logic']
        elif prev_question_node['type'] == 'multiple-choice':
            # Find the next question ID that matches the user's answer
            current_question_id = prev_question_node['next_question_logic'].get(user_message, 'final_summary') # Default to a safe end
        else: # Final node
            current_question_id = None
        
        session['current_question_id'] = current_question_id

    # --- Prepare the response ---
    if current_question_id:
        bot_response_node = TRIAGE_FLOW[current_question_id]
        bot_response = {
            "user_id": user_id,
            "bot_message": bot_response_node['question'],
            "options": bot_response_node.get('options', [])
        }
    else:
        # End of conversation
        # You could add logic here to summarize the answers for a doctor
        summary = user_sessions[user_id]['answers']
        print(f"Final summary for user {user_id}: {summary}") # Print to console for now
        bot_response = {
            "user_id": user_id,
            "bot_message": "Thank you. Your session is complete.",
            "options": []
        }

    return jsonify(bot_response)

if __name__ == '__main__':
    # Running the app on 0.0.0.0 makes it accessible on your local network
    app.run(host='0.0.0.0', port=5001, debug=True)