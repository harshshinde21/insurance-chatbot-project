from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import chatbot_nlp  # Import NLP model

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'local_storage/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('insurance.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign key constraints
    return conn

def handle_policy_status(user_input):
    policy_number = user_input.split()[-1]
    response = chatbot_nlp.get_policy_expiry(policy_number)
    return jsonify({"response": response})

def handle_claim_status(user_input):
    policy_number = user_input.split()[-1]
    response = chatbot_nlp.get_claim_status(policy_number)
    return jsonify({"response": response})

def handle_general_info(user_input):
    response = chatbot_nlp.generate_chatbot_response(user_input)
    return jsonify({"response": response})

@app.route('/')
def home():
    return "Welcome to the Insurance Chatbot API!"

@app.route('/recommend', methods=['POST'])
def recommend_policy():
    data = request.json
    name, age, conditions = data['name'], data['age'], data['health_conditions']
    
    policy = chatbot_nlp.get_policy_recommendation(conditions)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, health_conditions, recommended_policy) VALUES (?, ?, ?, ?)",
                   (name, age, conditions, policy))
    conn.commit()
    conn.close()
    
    return jsonify({'recommended_policy': policy})

@app.route('/submit_claim', methods=['POST'])
def submit_claim():
    data = request.json
    user_id, policy_id, amount = data['user_id'], data['policy_id'], data['amount']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO claims (user_id, policy_id, status, submission_date, amount) VALUES (?, ?, ?, datetime('now'), ?)",
                   (user_id, policy_id, "Pending", amount))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Claim submitted successfully'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("user_input", "").strip().lower()

        if not user_input:
            return jsonify({"response": "Please enter a message."}), 400

        if "policy" in user_input:
            return handle_policy_status(user_input)
        elif "claim" in user_input:
            return handle_claim_status(user_input)
        else:
            return handle_general_info(user_input)

    except Exception as e:
        return jsonify({"response": "Error processing request: " + str(e)}), 500

@app.route('/policy_status', methods=['POST'])
def policy_status():
    data = request.get_json()
    
    if not data or "policy_number" not in data:
        return jsonify({"response": "Error: No policy number provided. Please enter a valid policy number."}), 400
    
    policy_number = data["policy_number"]

    if not chatbot_nlp.validate_policy_number(policy_number):
        return jsonify({"response": "Invalid policy number format. Use POL12345."}), 400

    response = chatbot_nlp.get_policy_expiry(policy_number)
    return jsonify({"response": response})


@app.route('/check_claim_status/<int:claim_id>', methods=['GET'])
def check_claim_status(claim_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM claims WHERE claim_id = ?", (claim_id,))
    status = cursor.fetchone()
    conn.close()
    
    if status:
        return jsonify({'claim_status': status["status"]})
    return jsonify({'error': 'Claim not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
