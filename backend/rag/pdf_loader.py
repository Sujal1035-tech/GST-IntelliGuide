# backend/rag/pdf_loader.py

from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def load_and_split_pdfs(
    pdf_dir: str = "backend/rag/data",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Document]:

    base_path = Path(pdf_dir)
    if not base_path.exists():
        raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

    all_docs: List[Document] = []

    for pdf_path in base_path.glob("*.pdf"):
        print(f"Loading PDF: {pdf_path}")
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        all_docs.extend(docs)

    if not all_docs:
        raise ValueError("No PDF files found inside backend/rag/data")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    split_docs = splitter.split_documents(all_docs)

    print(f"Total chunks created: {len(split_docs)}")
    return split_docs
