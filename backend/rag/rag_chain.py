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

    prompt = ChatPromptTemplate.from_template("""You are a GST Expert for India. Answer using the provided context documents.

CRITICAL: Your response MUST follow this EXACT format. Do NOT deviate.

Format your response EXACTLY like this (copy this structure):

**🔹 Meaning / Definition**
• [Write 1-2 line definition here]

**🔹 When it Applies**
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]

**🔹 Rules / Conditions**
• [Rule 1 with section reference if available]
• [Rule 2]
• [Rule 3]

**🔹 Example**
• [Line 1 of example]
• [Line 2 of example]
• [Line 3 of example]

**🔹 Key Takeaway**
• [One sentence summary]

RULES:
1. ALWAYS start with **🔹 Meaning / Definition**
2. ALWAYS include all 5 sections in order
3. Use bullet points (•) for EVERY point
4. NO long paragraphs - break into bullets
5. If question is not GST-related, respond: "I don't know"

Context from GST documents:
{context}

User Question:
{question}

Your structured response:""")

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
