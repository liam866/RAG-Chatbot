# How It Works

The chatbot follows a simple Retrieval-Augmented Generation (RAG) pipeline.

## 1. Knowledge Base Ingestion

- On startup, the FastAPI backend scans the `kb/` directory for Markdown (`.md`) files.
- It parses each file into smaller chunks, divided by headings.
- Each chunk is stored in memory along with its metadata: the source file, the heading it belongs to, and the start and end line numbers.

## 2. User Query and Retrieval

- When a user sends a question via the `/chat` endpoint, the backend first searches the in-memory knowledge base for the most relevant chunks.
- This version uses a simple lexical search algorithm (BM25) to find chunks that best match the user's query.

## 3. Prompt Augmentation and Generation

- The top-k most relevant chunks are retrieved.
- These chunks are then inserted into a prompt that is sent to the Ollama LLM.
- The prompt instructs the model to answer the user's question *only* using the provided source text and to cite its sources.

## 4. Response and Citation

- The LLM generates an answer based on the provided context.
- The backend forwards this answer to the user, along with the source metadata (file, heading, lines) of the chunks that were used to generate the answer.
