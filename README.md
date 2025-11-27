<div align="center">

# 🏛️ GST IntelliGuide

### Intelligent AI Assistant for GST Compliance & Queries

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=22&duration=3000&pause=1000&color=009688&center=true&vCenter=true&width=600&lines=Real-time+GST+Query+Resolution;RAG-Powered+Knowledge+Base;WebSocket+Chat+Architecture;Production-Ready+AI+Application" alt="Typing SVG" />
</p>

</div>

---

## 📋 Overview

**GST IntelliGuide** is a conversational AI system that provides instant, accurate answers to GST (Goods and Services Tax) queries. Built with modern AI technologies, it combines Large Language Models with Retrieval-Augmented Generation (RAG) to deliver contextually accurate responses backed by official GST documentation.

### 💡 Key Capabilities
- Real-time conversational interface for GST queries
- Context-aware responses with source citations
- Secure user authentication and session management
- Persistent chat history across sessions
- WebSocket-based streaming responses

---

## ✨ Features

- **🔐 Secure Authentication**: JWT-based auth with HttpOnly cookies and password hashing
- **💬 Real-Time Chat**: WebSocket communication with streaming responses
- **🧠 RAG Pipeline**: Vector database semantic search with LangChain integration
- **📚 Multi-Chat Management**: Create, view, and manage multiple conversations
- **🎨 Modern UI**: Streamlit interface with auto-scroll and chat bubbles
- **📊 Persistent Storage**: MongoDB for users, chats, and message history
- **🔍 Source Attribution**: Transparent citations from GST documents

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (HTML/CSS/JS + WebSocket)     │
│   • Login/Register  • Chat Interface    │
└─────────────────────────────────────────┘
                  ↕ WS
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │   Auth   │  │  Chats   │  │  RAG  │ │
│  │ (JWT)    │  │ (CRUD)   │  │Pipeline│ │
│  └──────────┘  └──────────┘  └───────┘ │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│  MongoDB                FAISS           │
│  • users        • Document Embeddings   │
│  • chats        • Semantic Search       │
│  • messages                             │
└─────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

**Backend**
- **FastAPI**: High-performance async API framework with WebSocket support
- **LangChain**: LLM orchestration and RAG pipeline
- **FAISS**: Vector database for semantic search
- **JWT**: Stateless authentication
- **PyPDFLoader**: Document processing and chunking

**Frontend**
- **HTML/CSS/JavaScript**: Vanilla web interface with WebSocket support
- **Modern UI**: Responsive design with chat interface
- **WebSocket Client**: Real-time bidirectional communication

**Database**
- **MongoDB**: NoSQL database for users, chats, and messages
- **Vector Store**: Embeddings for GST documents

**AI/ML**
- **GroqAI**: Language model backends
- **Sentence Transformers**: Document embeddings

---

## 📦 Installation

### Prerequisites
```bash
Python 3.10+, MongoDB 6.0+, Git
```

### Quick Start

```bash
# Clone repository
git clone https://github.com/Sujal1035-tech/GST-IntelliGuide.git
cd GST-IntelliGuide

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pymongo motor langchain chromadb
pip install websockets pypdf sentence-transformers
pip install python-jose[cryptography] passlib[bcrypt] python-dotenv

# Configure environment
cp .env.example .env
# Edit .env with your configurations

# Start MongoDB
# Linux: sudo systemctl start mongod
# Windows: Start MongoDB service

# Run Backend
cd backend
uvicorn main:app --reload --port 8000

# Open Frontend
# Open frontend/login.html in your browser
# Or serve with: python -m http.server 8080 (in frontend folder)
```

### Environment Configuration (.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=gst_intelliguide
SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=your-api-key
```

---

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login (returns JWT cookie)

### Chat Management
- `POST /chats/` - Create new chat
- `GET /chats/` - List user's chats
- `GET /chats/{chat_id}/messages` - Get chat history
- `DELETE /chats/{chat_id}` - Delete chat

### WebSocket
- `WS /ws/chat/{chat_id}` - Real-time chat communication

### Utility
- `GET /ping` - Health check
- `GET /docs` - Interactive API documentation

**Full API Documentation**: http://localhost:8000/docs

---

## 📂 Project Structure

```
GST-IntelliGuide/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration settings
│   ├── auth/                # Authentication module
│   ├── chats/               # Chat management
│   ├── db/                  # Database operations
│   └── rag/                 # RAG pipeline
│
├── frontend/
│   ├── chat.html            # Chat interface
│   ├── chat.js              # Chat logic
│   ├── login.html           # Login page
│   ├── login.js             # Login logic
│   ├── register.html        # Registration page
│   ├── register.js          # Registration logic
│   └── style.css            # Styling
│
├── .env                     # Environment variables
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md                # Documentation

```
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Sujal Khant** - AI Engineer | ML Specialist

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Sujal1035-tech)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](www.linkedin.com/in/sujal-khant-234931356)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:your.sujalkhant4@gmail.com)

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Built with ❤️ for simplifying GST compliance**

</div>

```

