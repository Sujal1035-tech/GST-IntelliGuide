from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 60))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_EMBEDDING_MODEL = os.getenv(
    "HF_EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)
