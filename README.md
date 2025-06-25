🚀 Mero Nepali Bot – Nepali Chatbot with OpenAI API

A simple Nepali chatbot built using Flask, OpenAI API, and SQLite. This chatbot allows users to have conversations in Nepali while storing user history in a database.

🖥️ Features
🌐 Web-based chatbot UI with light/dark mode.

💡 Supports Nepali prompts and conversations.

🔐 Stores user conversation history using SQLite.

🔗 Powered by OpenAI API for responses.

🗂️ Basic user management with persistent storage.

🔧 Tech Stack
Backend: Python, Flask, SQLite

Frontend: HTML, CSS, JavaScript

API: OpenAI API

📦 Installation
1️⃣ Clone the repository:

```bash

git clone https://github.com/yourusername/mero-nepali-bot.git
cd mero-nepali-bot
```

2️⃣ Set up a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3️⃣ Install dependencies:

```bash
pip install -r requirements.txt
```

4️⃣ Create a .env file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

5️⃣ Run the app:
```bash
python app.py
```

6️⃣ Open your browser and go to:
http://127.0.0.1:3000

🗄️ Database Info
SQLite database: user_data.db

Table: users

id (Primary Key)

user_name (Text)

message_history (Text)

🛑 .gitignore
Make sure your .gitignore file includes:

```bash
.env
__pycache__/
*.pyc
```
user_data.db
🎯 Future Improvements
User authentication system

Speech-to-text for Nepali input

Deployment to cloud platforms (Render, Heroku, Vercel)

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
