import os
import bs4
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools import tool
from langchain_classic import hub
# NEW
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

async def generate_rag_summary(url: str):
# Retrieve key explicitly to verify its existence
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise ValueError("GROQ_API_KEY is missing in your .env file!")

    # Pass the key explicitly
    llm = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0,
        groq_api_key=groq_key
    )
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Updated Strainer to be more generic and include Wikipedia content
    # Wikipedia uses #content or #bodyContent. General sites use <main> or <article>.
    bs4_strainer = bs4.SoupStrainer(
        name=("main", "article", "div", "h1", "h2", "h3", "p"),
        attrs={"id": ["content", "bodyContent", "main-content"], "class": ["post-content", "entry-content", "article-body"]}
    )

    # Fallback: If strict filtering misses content, we might want to just grab body text or specific tags.
    # For now, let's grab specific tags regardless of class if they are structural text.
    bs4_strainer = bs4.SoupStrainer(name=("p", "h1", "h2", "h3", "h4", "li", "article", "main"))

    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)

    # 3. Create Vector Store
    vector_store = InMemoryVectorStore.from_documents(all_splits, embeddings)

    # 4. Retrieve Context (Simple RAG)
    # We use a direct retrieval instead of an agent to save tokens and avoid Rate Limits (6k TPM)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2}) # Top 2 chunks only
    retrieved_docs = retriever.invoke("Summary of the main topic and key points")
    
    # Combine content
    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # 5. Direct LLM Call (No Agent Overhead)
    system_prompt = (
        "You are an expert summarizer. Analyze the provided text and generate a structured summary "
        "including Key Insights, Main Points, and a Conclusion. Use Markdown formatting. "
        "Keep the summary concise and professional."
    )
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context:\n{context_text}\n\nInstruction: Summarize the content above.")
    ]
    
    response = llm.invoke(messages)
    
    return response.content