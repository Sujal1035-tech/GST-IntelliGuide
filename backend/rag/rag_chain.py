import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from backend import config

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
def get_rag_chain():

    embeddings = HuggingFaceEmbeddings(
        model_name=config.HF_EMBEDDING_MODEL
    )

    vectorstore = FAISS.load_local(
        folder_path="backend/rag/faiss_index",
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0.0
    )

    prompt = ChatPromptTemplate.from_template("""
You are an expert GST (Goods and Services Tax) consultant for India. Your role is to provide accurate, helpful answers based solely on the provided context.

**Instructions:**
1. Answer questions using ONLY the information from the context below
2. If the context contains relevant information, provide a clear, detailed explanation
3. If the answer is not in the context, respond: "I don't have information about this in the available GST documents. Please consult with a tax professional or refer to official GST resources."
4. Be specific and cite relevant sections, rules, or forms when mentioned in the context
5. Use simple language and explain technical terms when possible
6. If the question is partially answered, provide what you know and mention what's missing

Context:
{context}

Question:
{question}
""")

    rag_chain = (
        {
            
            "context": (lambda x: x["question"]) | retriever, 
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
