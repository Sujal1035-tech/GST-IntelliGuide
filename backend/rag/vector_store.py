# backend/rag/vector_store.py

from pathlib import Path
from typing import Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from backend.rag.pdf_loader import load_and_split_pdfs
from backend.config import HF_EMBEDDING_MODEL


INDEX_DIR = Path("backend/rag/faiss_index")


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=HF_EMBEDDING_MODEL)


def build_faiss_index(docs: Optional[list[Document]] = None):
    embeddings = get_embeddings()

    if docs is None:
        docs = load_and_split_pdfs()

    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(docs, embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))

    print("FAISS successfully saved!")
    return vectorstore


def load_or_build_faiss_index():
    embeddings = get_embeddings()

    if INDEX_DIR.exists():
        print("Loading FAISS index...")
        return FAISS.load_local(
            str(INDEX_DIR), embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("FAISS index missing — building new one...")
        return build_faiss_index()
    
    
if __name__ == "__main__":
    print("--- Starting FAISS Index Build ---")
    try:
        # Use load_or_build_faiss_index() to handle missing index automatically
        load_or_build_faiss_index()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure your PDF file (e.g., gst_pdf2.pdf) exists in backend/rag/data/")
    except Exception as e:
        print(f"An unexpected error occurred during index build: {e}")
    print("--- FAISS Index Build Process Complete ---")