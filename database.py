import sqlite3

def init_db():
    conn = sqlite3.connect('insurance.db')
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        health_conditions TEXT,
                        recommended_policy TEXT
                    )''')
    
    # Policies Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS policies (
                        policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        policy_type TEXT NOT NULL,
                        start_date TEXT,
                        end_date TEXT,
                        premium_amount REAL
                    )''')
    
    # Claims Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS claims (
                        claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        policy_id INTEGER,
                        status TEXT DEFAULT 'Pending',
                        submission_date TEXT DEFAULT CURRENT_TIMESTAMP,
                        amount REAL,
                        FOREIGN KEY(user_id) REFERENCES users(id),
                        FOREIGN KEY(policy_id) REFERENCES policies(policy_id)
                    )''')
    
    # Chatbot Logs Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS chatbot_logs (
                        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                        query_text TEXT,
                        response_text TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_db()
