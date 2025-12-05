<div align="center">

# GST IntelliGuide

### AI-Powered GST Compliance Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

### [**Try Live Demo**](https://gst-intelliguide-latest.onrender.com)

*Note: Deployed on Render free tier - first load may take 30-50 seconds*

</div>

---

## Overview

GST IntelliGuide is an intelligent chatbot that answers GST-related questions using RAG (Retrieval-Augmented Generation) technology. Ask questions in natural language and receive accurate answers with document citations.

The application searches through official GST documents and provides context-aware responses, eliminating the need to manually review lengthy PDFs and regulations.

## Key Features

**Contextual Understanding** - Uses semantic search with FAISS vector database to understand query intent, not just keywords. Powered by RAG architecture for accurate, document-backed responses.

**Conversation Memory** - Implements LangChain's ConversationBufferWindowMemory to maintain context across messages within a chat session, enabling natural multi-turn conversations.

**Real-time Streaming** - WebSocket-based architecture delivers responses as they're generated, providing immediate feedback and a smooth user experience.

**Persistent Chat History** - All conversations are stored in MongoDB with proper user isolation. Create multiple chat sessions organized by topic for easy reference.

**Secure Authentication** - JWT-based authentication with bcrypt password hashing. HTTP-only cookies prevent XSS attacks and ensure session security.

**Docker Deployment** - Containerized application ensures consistency across development and production environments. Currently deployed on Render cloud platform.

## Technology Stack

**Backend**: FastAPI, LangChain (with ConversationBufferWindowMemory), FAISS, GroqAI

**Frontend**: Vanilla JavaScript, HTML5, CSS3

**Database**: MongoDB Atlas

**Deployment**: Docker, Render

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Sujal1035-tech/GST-IntelliGuide.git
cd GST-IntelliGuide
```

Create environment file:

```bash
cp .env.example .env
```

Configure your .env:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=gst_intelliguide
SECRET_KEY=your-secure-secret-key
OPENAI_API_KEY=your-groq-api-key
```

Run with Docker:

```bash
docker-compose up --build
```

Access at http://localhost:8000 (backend) and http://localhost:8080 (frontend).

## Architecture

The application uses a multi-layered architecture:

**RAG Pipeline** - User queries are converted to embeddings and matched against pre-indexed GST documents in FAISS. Retrieved context is combined with the query and sent to GroqAI for response generation.

**Memory Management** - LangChain's ConversationBufferWindowMemory maintains the last N messages in each chat session, allowing the AI to reference previous exchanges and maintain conversation flow.

**Real-time Communication** - WebSocket connections handle bidirectional streaming between client and server, enabling token-by-token response delivery.

**Data Persistence** - MongoDB stores user credentials, chat sessions, and message history with proper indexing for efficient retrieval.

## Project Structure

```
GST-IntelliGuide/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── auth/                # JWT authentication
│   ├── chats/               # Chat CRUD operations
│   ├── db/                  # MongoDB connection
│   └── rag/                 # RAG pipeline with memory
│
├── frontend/
│   ├── chat.html            # Chat interface
│   ├── login.html           # Authentication
│   └── style.css            # Styling
│
└── docker-compose.yml       # Container orchestration
```

## Deployment

The application is deployed at [gst-intelliguide-latest.onrender.com](https://gst-intelliguide-latest.onrender.com) using:

- MongoDB Atlas for database hosting
- Render for containerized application hosting
- Docker for consistent deployment environment

To deploy your own instance, configure MongoDB Atlas, create a Render web service from your GitHub repository, set environment variables, and enable auto-deploy.

## Contributing

Fork the repository, create a feature branch, implement changes, and submit a pull request. Ensure code follows existing patterns and includes proper error handling.

## License

MIT License - See LICENSE file for details.

## Author

**Sujal Khant**

GitHub: [Sujal1035-tech](https://github.com/Sujal1035-tech)  
LinkedIn: [sujal-khant-234931356](https://www.linkedin.com/in/sujal-khant-234931356)  
Email: sujalkhant4@gmail.com

---

<div align="center">

Built to simplify GST compliance for everyone

</div>
