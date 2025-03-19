import nltk
from nltk.tokenize import word_tokenize
import random
import json
import datetime
import sqlite3
import re

nltk.download('punkt')

# Load predefined policy mapping from a JSON file (to allow easy updates)
def load_policy_mapping():
    try:
        with open("policy_mapping.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "diabetes": "Diabetes Care Plan",
            "heart": "Cardiac Protection Plan",
            "cancer": "Critical Illness Cover",
            "accident": "Personal Accident Insurance",
            "general": "Standard Health Plan"
        }

def get_db_connection():
    conn = sqlite3.connect('insurance.db')
    conn.row_factory = sqlite3.Row
    return conn

def validate_policy_number(policy_number):
    return bool(re.match(r"^POL[0-9]{5}$", policy_number))

def get_policy_recommendation(conditions):
    conditions = word_tokenize(conditions.lower())
    policy_mapping = load_policy_mapping()
    
    matched_policies = [policy for condition, policy in policy_mapping.items() if condition in conditions]
    
    return matched_policies if matched_policies else ["Comprehensive Health Coverage"]

def generate_chatbot_response(user_input):
    greetings = ["hello", "hi", "hey", "greetings"]
    if any(word in user_input.lower() for word in greetings):
        return "Hello! How can I assist you with your insurance today?"
    
    if "policy" in user_input.lower():
        return "Can you provide details about your health conditions so I can recommend the best insurance plan?"
    
    if "claim" in user_input.lower():
        return "I can help you with claim submission and status tracking. Please provide your policy number."
    
    if "premium" in user_input.lower():
        return "Insurance premiums depend on multiple factors such as age, health conditions, and coverage. Would you like a quote?"
    
    if "renew" in user_input.lower():
        return "I can guide you through the renewal process. Please provide your policy number."
    
    if "coverage" in user_input.lower():
        return "Coverage details vary by plan. Would you like me to fetch the coverage details for a specific policy?"
    
    return "I'm not sure how to respond to that. Could you please provide more details?"

def get_insurance_quote(age, health_conditions):
    base_price = 5000  # Base premium amount
    age_factor = (age - 18) * 50  # Increase premium based on age
    condition_factor = len(health_conditions.split()) * 300  # Increase based on number of conditions
    
    premium = base_price + age_factor + condition_factor
    return f"Estimated insurance premium: ${premium} per year."

def get_claim_status(policy_number):
    if not validate_policy_number(policy_number):
        return "Invalid policy number format. Please provide a valid policy number (e.g., POL12345)."
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM claims WHERE policy_id = ?", (policy_number,))
    status = cursor.fetchone()
    conn.close()
    
    return f"The current status of policy {policy_number} is: {status['status']}" if status else "No claim found for this policy."

def get_policy_expiry(policy_number):
    if not validate_policy_number(policy_number):
        return "Invalid policy number format. Please provide a valid policy number (e.g., POL12345)."
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT end_date FROM policies WHERE policy_id = ?", (policy_number,))
    expiry_date = cursor.fetchone()
    conn.close()
    
    return f"Your policy {policy_number} is set to expire on {expiry_date['end_date']}. Please renew it on time." if expiry_date else "No policy found."

def log_chatbot_interaction(user_id, query_text, response_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chatbot_logs (user_id, timestamp, query_text, response_text) VALUES (?, datetime('now'), ?, ?)",
                   (user_id, query_text, response_text))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    test_conditions = "I have diabetes and heart problems"
    print("Recommended Policy:", get_policy_recommendation(test_conditions))
    
    test_input = "Hello, I need help with my insurance"
    print("Chatbot Response:", generate_chatbot_response(test_input))
    
    print(get_insurance_quote(35, "diabetes heart"))
    print(get_claim_status("POL12345"))
    print(get_policy_expiry("POL12345"))
