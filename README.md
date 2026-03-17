# Local RAG FAQ Chatbot

FAQ-Chatbot is a containerised retrieval-augmented chatbot that answers questions using a local document knowledge base. It retrieves relevant document chunks, embeds them in a vector store, and feeds them to a local LLM to generate grounded, verifiable answers. Every response includes citations to the source documents, reducing hallucinations and ensuring transparency.

The project demonstrates a modular RAG pipeline with a focus on reliability, explainability and fully local deployment.

---

## Problem & Solution

Large Language Models (LLMs) are powerful but often hallucinate, producing confident but incorrect answers. FAQ-Chatbot addresses this by:

- Grounding answers in an local, auditable knowledge base (Markdown files).  
- Refusing to answer when retrieved evidence is insufficient.
- Returning answers with explicit citations to document source, heading and line range.
---

## How It Works

The system is built as a decoupled, containerised pipeline:

### Document Ingestion & Sync

- Markdown files in /kb are parsed and chunked by headings.
- Chunks are hashed and synced with a persistent vector store (ChromaDB).
- Only new or modified chunks are updated, reducing overhead.

### Embedding & Semantic Search

- Chunks are embedded using a local Ollama embedding model (all-minilm:22m).
- User queries are embedded and matched to chunks using cosine similarity.
- A configurable relevance threshold ensures only high-confidence chunks are used.

### LLM Generation

- Retrieved chunks are provided as context to a local Ollama LLM (qwen2.5:7b-instruct).
- Answers are strictly grounded in retrieved documents.
- Responses include source citations for each referenced chunk.

### API & Debugging

- FastAPI service handles queries and returns structured answers with citations.
- Debug endpoints allow inspection of retrieved chunks, similarity scores, and relevance filtering.

---

## Key Features

- **Fully Local & Private:** No data leaves your environment.  
- **Retrieval-Augmented Generation:** Answers are grounded in the knowledge base.
- **Modular Pipeline:** Decoupled ingestion, embedding, vector search, and LLM inference.
- **Persistent Vector Store:** ChromaDB stores embeddings locally (./chroma_data).
- **Similarity Filtering:** Low-confidence chunks are filtered for reliable responses.
- **Debugging & Inspectability:** Endpoints provide transparency into retrieval and scoring.
- **Citation-Based Responses:** Every answer includes document references to ensure traceability.

---

## Prerequisites

- Docker & Docker Compose installed  
- Ollama installed locally with required models:

```sh
ollama pull qwen2.5:7b-instruct
ollama pull all-minilm:22m
```

- Run the Service:
  
```sh
    docker compose up --build
 ```

## Usage & Testing

- Health Check: Confirm service is running and check Ollama models.
  
```sh
curl -s http://localhost:8000/health | jq .
```

- Chat Endpoint: Ask a question and get grounded responses with citations.

```sh
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"What is this project for?"}' | jq .
```

## Possible Extensions
- Multi-user support and authentication
- Expanded knowledge bases with structured metadata
- Conversational or multi-turn query support
- Real-time update and monitoring of document ingestion
- Enhanced analytics on retrieval quality and coverage
