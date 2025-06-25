from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import sqlite3
import os
import time
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY","your_openai_api_key_here")

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Retrieve user data from the database
def get_user_data(user_name):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_name = ?', (user_name,)).fetchone()
    conn.close()
    return user

# Store user data in the database
def store_user_data(user_name, message):
    conn = get_db_connection()
    user = get_user_data(user_name)

    if user:
        new_history = user['message_history'] + "\n" + message
        conn.execute('UPDATE users SET message_history = ? WHERE user_name = ?', (new_history, user_name))
    else:
        conn.execute('INSERT INTO users (user_name, message_history) VALUES (?, ?)', (user_name, message))

    conn.commit()
    conn.close()

# Ensure the database table exists
def create_table():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            message_history TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call create_table() before starting the server
create_table()

@app.route("/")
def index():
    return send_from_directory("", "index.html")

@app.route("/styles.css")
def styles():
    return send_from_directory("", "styles.css")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    user_name = request.json.get("user_name", "")

    if not user_message or not user_name:
        return jsonify({"error": "Message and user_name are required"}), 400

    user = get_user_data(user_name)

    # Initialize message history if user data doesn't exist
    if user:
        message_history = user['message_history'].split("\n")
    else:
        message_history = []

    # Append the new user message to the history
    message_history.append(user_message)
    store_user_data(user_name, user_message)

    creator_keywords = [
        "who created you", "who made you", "who is your creator", "who developed you",
        "made by", "created by", "who made you?", "who developed you?", "who is your creator?",
        "koslea banako tmlai", "koslea banako talai", "koslea banako tapailai", "koslea yojana gareko", "banako"
    ]
    
    if any(keyword in user_message.lower() for keyword in creator_keywords):
        if "who created you" in user_message.lower() or "who made you" in user_message.lower():
            return jsonify({"reply": "I was created by Bipin Mahat."})
        else:
            return jsonify({"reply": "Ma Bipin Mahat dwara banaiyeko srijana ho."})

    try:
        # Send the conversation history to OpenAI for a response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Ma Roman Nepali ma bolne chatbot ho."}]
            + [{"role": "user", "content": msg} if idx % 2 == 0 else {"role": "assistant", "content": msg}
               for idx, msg in enumerate(message_history)]
        )

        bot_reply = response["choices"][0]["message"]["content"]
        store_user_data(user_name, bot_reply)

        return jsonify({"reply": bot_reply})
    except openai.error.RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        time.sleep(5)
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"OpenAI API Error: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
