import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings
from typing import List

from .kb import load_knowledge_base
from .vector_store import VectorStore
from .retrieval import Retriever
from .ollama_client import OllamaClient, OllamaError
from .schemas import ChatRequest, ChatResponse, Source, DocumentChunk

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    ollama_base_url: str = "http://host.docker.internal:11434"
    ollama_llm_model: str = "qwen2.5:7b-instruct"
    ollama_embed_model: str = "all-minilm:22m"
    top_k: int = 3

settings = Settings()
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Global instances
VECTOR_STORE: VectorStore = None
RETRIEVER: Retriever = None
OLLAMA_CLIENT: OllamaClient = None

def build_prompt(question: str, context_chunks: List[DocumentChunk]) -> str:
    if not context_chunks:
        return f"I do not have any information in my knowledge base to answer: '{question}'."

    context = "\n\n---\n\n".join([chunk.text for chunk in context_chunks])
    
    return f"""
    SYSTEM: You are a strict FAQ bot. You must answer the question using ONLY the provided context.
    RULES:
    1. If the answer is NOT in the context, you MUST say "I don't know based on my files."
    2. Do NOT use your own outside knowledge
    3. If the context is irrelevant to the question, say "I don't know."

    CONTEXT:
    {context}

    USER QUESTION: 
    {question}
    
    ANSWER:
    """

@app.on_event("startup")
def startup_event():
    global VECTOR_STORE, RETRIEVER, OLLAMA_CLIENT
    
    logger.info("Initializing ChromaDB vector store...")
    VECTOR_STORE = VectorStore(
        path="chroma_data",
        ollama_base_url=settings.ollama_base_url,
        embed_model=settings.ollama_embed_model
    )
    
    logger.info("Synchronizing knowledge base with vector store...")
    kb_chunks = load_knowledge_base(kb_dir="kb")
    VECTOR_STORE.sync_documents(kb_chunks)
    
    logger.info("Initializing retriever...")
    RETRIEVER = Retriever(VECTOR_STORE)
    
    logger.info("Initializing Ollama client...")
    OLLAMA_CLIENT = OllamaClient(settings.ollama_base_url, settings.ollama_llm_model)
    logger.info("Startup complete.")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "ollama_base_url": settings.ollama_base_url,
        "ollama_llm_model": settings.ollama_llm_model,
        "ollama_embed_model": settings.ollama_embed_model,
    }

@app.post("/chat", response_model=ChatResponse)
def chat_handler(chat_request: ChatRequest):
    logger.info(f"Received question: {chat_request.question}")
    
    retrieved_docs = RETRIEVER.search(query=chat_request.question, top_k=settings.top_k)
    
    prompt = build_prompt(chat_request.question, retrieved_docs)
    
    try:
        answer = OLLAMA_CLIENT.generate(prompt)
    except OllamaError as e:
        logger.error(f"Error from Ollama client: {e}")
        raise HTTPException(status_code=503, detail=str(e))
        
    sources = [
        Source(
            file=doc.file,
            heading=doc.heading,
            start_line=doc.start_line,
            end_line=doc.end_line
        ) for doc in retrieved_docs
    ]
    
    return ChatResponse(answer=answer, sources=sources)
