from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from g4f.client import Client
import os

app = Flask(__name__)
CORS(app)  # Allow all origins to access the API

# Set a secret key for session management
app.secret_key = 'APP123'

# Initialize G4F Client
client = Client()

# Load and preprocess custom knowledge
def load_custom_knowledge(file_path):
    """Load and preprocess custom knowledge from a text file."""
    with open(file_path, 'r') as f:
        knowledge = f.read()
    return knowledge.strip()

# Load the custom knowledge base into a global variable
custom_knowledge = load_custom_knowledge("custom_knowledge.txt")

@app.route('/')
def home():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"reply": "Message cannot be empty."}), 400

        # Retrieve conversation history from session
        messages = session.get('messages', [])

        # Add a system message if this is the first message in the conversation
        if not messages:
            system_message = {
                "role": "system",
                "content": (
                    "You are an intelligent chatbot with access to the following custom knowledge:\n\n"
                    f"{custom_knowledge}\n\n"
                    "Use this knowledge to answer questions accurately. If the information is not in the custom "
                    "knowledge, use your general training to respond appropriately. Always prioritize being accurate and helpful."
                )
            }
            messages.append(system_message)

        # Append the user's message to the conversation history
        messages.append({"role": "user", "content": user_message})

        # Get GPT's response
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
        )

        # Extract the GPT response
        gpt_response = response.choices[0].message.content
        messages.append({"role": "system", "content": gpt_response})

        # Save updated conversation history back to session
        session['messages'] = messages

        return jsonify({"reply": gpt_response})
    except Exception as e:
        return jsonify({"reply": f"Error generating response: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
