<div align="center">

# 🏛️ GST IntelliGuide

### Your Smart Companion for GST Questions & Compliance

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=22&duration=3000&pause=1000&color=009688&center=true&vCenter=true&width=600&lines=Get+Instant+GST+Answers;Powered+by+RAG+Technology;Real-Time+Chat+Interface;Production-Ready+Solution" alt="Typing SVG" />
</p>

</div>

---

## 📋 What's This All About?

Ever found yourself confused about GST rules and regulations? Yeah, me too. That's why I built **GST IntelliGuide** - it's basically a chatbot that actually understands GST documentation and gives you straight answers without the legal jargon.

Think of it as having a GST expert available 24/7 who can instantly search through all the official documents and explain things in plain English. No more digging through hundred-page PDFs at midnight!

### 💡 What Can It Do?
- Chat naturally about GST - ask questions like you would to a friend
- Get answers backed by actual GST documents (with citations!)
- Keep track of all your conversations for future reference
- Login securely and access your chat history from anywhere
- Enjoy real-time responses that stream in as they're generated

---

## ✨ Cool Features

- **🔐 Security First**: Your data is protected with JWT authentication and encrypted passwords
- **💬 Live Conversations**: Uses WebSocket technology for that smooth, instant messaging feel
- **🧠 Smart Search**: Doesn't just keyword match - actually understands what you're asking
- **📚 Organized Chats**: Start different conversations for different topics, keep everything neat
- **🎨 Clean Interface**: Simple HTML/CSS/JavaScript - no fancy frameworks needed
- **📊 Saves Everything**: All your chats and messages stored safely in MongoDB
- **🔍 Shows Sources**: Every answer comes with references to the actual GST documents

---

## 🏗️ How It Works

Here's the basic flow of how everything connects:

```
┌─────────────────────────────────────────┐
│     Web Browser (Your End)              │
│   Login → Chat → Get Answers            │
└─────────────────────────────────────────┘
                  ↕ WebSocket
┌─────────────────────────────────────────┐
│         FastAPI Server                  │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │  Login   │  │   Chat   │  │  AI   │ │
│  │  System  │  │ Manager  │  │Engine │ │
│  └──────────┘  └──────────┘  └───────┘ │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│  MongoDB Storage     FAISS Search       │
│  (users, chats)      (GST documents)    │
└─────────────────────────────────────────┘
```

Basically: You ask a question → AI searches the documents → Finds relevant info → Generates an answer → Sends it back to you in real-time.

---

## 🛠️ Tech Stack (For the Curious)

**Backend Stuff**
- **FastAPI**: Super fast Python framework that handles all the API requests
- **LangChain**: Manages the AI workflow and document retrieval
- **FAISS**: Vector database that enables semantic search (fancy way of saying "smart search")
- **JWT**: Handles secure authentication without storing sessions
- **PyPDFLoader**: Reads and processes GST PDF documents

**Frontend Stuff**
- **HTML/CSS/JavaScript**: Good old vanilla web technologies, nothing complicated
- **WebSocket**: Enables that real-time chat experience
- **Responsive Design**: Works on desktop, tablet, and mobile

**Database**
- **MongoDB**: Stores user accounts, chat histories, and messages
- **Vector Store**: Keeps all the GST document embeddings for quick search

**AI Components**
- **GroqAI**: Powers the language model responses
- **Sentence Transformers**: Creates embeddings from documents for semantic search

---

## 📦 Getting Started

### What You'll Need
- Python 3.10 or higher
- MongoDB 6.0 or higher
- Git (for cloning the repo)
- A cup of coffee (optional but recommended ☕)

### Installation Steps

```bash
# First, grab the code
git clone https://github.com/Sujal1035-tech/GST-IntelliGuide.git
cd GST-IntelliGuide

# Set up a virtual environment (keeps things clean)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install all the required packages
pip install fastapi uvicorn pymongo motor langchain faiss-cpu
pip install websockets pypdf sentence-transformers
pip install python-jose[cryptography] passlib[bcrypt] python-dotenv

# Create your environment file
cp .env.example .env
# Open .env and add your API keys and settings

# Make sure MongoDB is running
# On Linux: sudo systemctl start mongod
# On Windows: Start it from Services or MongoDB Compass

# Fire up the backend server
cd backend
uvicorn main:app --reload --port 8000

# Open the frontend
# Just open frontend/login.html in your browser
# Or if you want a local server: python -m http.server 8080
```

### Setting Up Your Environment (.env)

Create a `.env` file with these settings:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=gst_intelliguide
SECRET_KEY=make-this-something-random-and-secure
OPENAI_API_KEY=your-groq-or-openai-key-here
```

**Pro tip**: Never commit your `.env` file to git. It's already in `.gitignore`, so you're safe!

---

## 📡 API Routes

Here's what the backend can do:

### User Authentication
- `POST /auth/register` - Sign up for a new account
- `POST /auth/login` - Log in (sets a secure cookie with your token)

### Managing Your Chats
- `POST /chats/` - Start a new conversation
- `GET /chats/` - See all your previous chats
- `GET /chats/{chat_id}/messages` - Load messages from a specific chat
- `DELETE /chats/{chat_id}` - Delete a chat you don't need anymore

### Real-Time Communication
- `WS /ws/chat/{chat_id}` - WebSocket endpoint for live chatting

### Other Stuff
- `GET /ping` - Quick health check to see if server is alive
- `GET /docs` - Interactive API documentation (FastAPI gives this for free!)

**Want to explore?** Once the server is running, visit http://localhost:8000/docs for an interactive API playground.

---

## 📂 Project Layout

Here's how everything is organized:

```
GST-IntelliGuide/
├── backend/
│   ├── __init__.py
│   ├── main.py              # Where the magic starts
│   ├── config.py            # All the settings in one place
│   ├── auth/                # Login/signup logic
│   ├── chats/               # Chat operations
│   ├── db/                  # Database connections
│   └── rag/                 # The AI brain
│
├── frontend/
│   ├── chat.html            # Main chat page
│   ├── chat.js              # Chat functionality
│   ├── login.html           # Login page
│   ├── login.js             # Login handlers
│   ├── register.html        # Sign up page
│   ├── register.js          # Registration handlers
│   └── style.css            # All the styling
│
├── .env                     # Your secret keys (don't share!)
├── .gitignore               # Files git should ignore
├── requirements.txt         # Python dependencies
└── README.md                # You're reading it!
```

Each folder has a specific job, making the code easy to navigate and maintain.

---

## 📄 License

This project is open source under the MIT License. Check out the [LICENSE](LICENSE) file for the legal details. 

TLDR: Feel free to use it, modify it, or build upon it. Just give credit where it's due!

---

## 👨‍💻 About Me

Hey! I'm **Sujal Khant**, and I built this while trying to make sense of GST regulations myself. If this project helps you, that makes it all worth it!

Feel free to reach out:

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Sujal1035-tech)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sujal-khant-234931356)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:sujalkhant4@gmail.com)

Got questions? Found a bug? Want to contribute? Don't hesitate to open an issue or send a pull request!

<div align="center">

### ⭐ If this helped you, give it a star!

**Made with ❤️ and lots of GST confusion**

</div>
