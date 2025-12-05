import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from backend import config

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Cache for expensive components (loaded once)
_embeddings = None
_vectorstore = None
_llm = None

def _get_components():
    """Lazy load expensive components once"""
    global _embeddings, _vectorstore, _llm
    
    if _embeddings is None:
        print("🔄 Loading embeddings model...")
        _embeddings = HuggingFaceEmbeddings(
            model_name=config.HF_EMBEDDING_MODEL
        )
    
    if _vectorstore is None:
        print("🔄 Loading FAISS index...")
        _vectorstore = FAISS.load_local(
            folder_path="backend/rag/faiss_index",
            embeddings=_embeddings,
            allow_dangerous_deserialization=True,
        )
    
    if _llm is None:
        print("🔄 Initializing LLM...")
        _llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )
    
    return _embeddings, _vectorstore, _llm


# In-memory chat history store (per session)
# For production, this is backed by MongoDB in websocket.py
_chat_histories: dict[str, list] = {}

def get_chat_history(chat_id: str, max_messages: int = 20) -> str:
    """Get formatted chat history for a chat session"""
    if chat_id not in _chat_histories:
        return "(New conversation)"
    
    history = _chat_histories[chat_id][-max_messages:]  # Last N messages
    
    if not history:
        return "(New conversation)"
    
    formatted = []
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        content = msg["content"][:300] + "..." if len(msg["content"]) > 300 else msg["content"]
        formatted.append(f"{role}: {content}")
    
    return "\n".join(formatted)


def add_to_history(chat_id: str, role: str, content: str):
    """Add a message to chat history"""
    if chat_id not in _chat_histories:
        _chat_histories[chat_id] = []
    
    _chat_histories[chat_id].append({
        "role": role,
        "content": content
    })
    
    # Keep only last 20 messages to prevent memory issues
    if len(_chat_histories[chat_id]) > 20:
        _chat_histories[chat_id] = _chat_histories[chat_id][-20:]


def get_rag_response(chat_id: str, question: str) -> str:
    """
    Get RAG response with automatic memory management.
    Uses in-memory buffer with window limit.
    """
    _, vectorstore, llm = _get_components()
    
    # Get retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # Get chat history
    chat_history = get_chat_history(chat_id)
    
    # Add user question to history
    add_to_history(chat_id, "user", question)
    
    # Retrieve context
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template("""You are GST IntelliGuide - an AI assistant EXCLUSIVELY for Indian GST laws.

=== CRITICAL RULE ===
You MUST ONLY answer questions about GST, Indian taxation, CGST, SGST, IGST, tax compliance.
You MUST REFUSE programming, general knowledge, or non-tax questions politely.

=== CONVERSATION HISTORY ===
{chat_history}

=== USER MESSAGE ===
{question}

=== GST KNOWLEDGE ===
{context}

=== RESPONSE RULES ===
1. If NOT about GST → "I'm GST IntelliGuide, I specialize in Indian GST only. How can I help with GST?"
2. For greetings → Warm response
3. For follow-ups ("one line", "more detail") → Apply to previous topic from history
4. For simple questions → 2-4 sentences with bullets
5. For complex topics → Use structured format with 🔹 headers

Your response:""")
    
    # Build and run chain
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "chat_history": chat_history,
        "question": question,
        "context": context
    })
    
    # Add bot response to history
    add_to_history(chat_id, "assistant", response)
    
    return response
