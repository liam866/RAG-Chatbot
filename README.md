# Local RAG FAQ Chatbot

A self-contained FAQ chatbot designed to run entirely locally via Docker Compose. It uses a local Ollama instance to perform Retrieval-Augmented Generation (RAG) over a Markdown-based knowledge base, delivering verifiable answers grounded in your documents.

---

## Problem & Solution

Large Language Models (LLMs) often hallucinate - providing confident but incorrect answers without verifiable sources. This project tackles that by:

- **Grounding answers in an auditable, local knowledge base** (Markdown files).  
- **Refusing to answer when evidence is insufficient**, preventing misinformation.  
- **Including precise citations** for every response, ensuring traceability.

---

## How It Works

The chatbot implements a standard RAG pipeline:

1. **Ingestion & Sync**  
   On startup, Markdown files in `/kb` are parsed, chunked by headings, hashed, and synchronized with a persistent vector store (ChromaDB). Only new or changed chunks are updated.

2. **Embedding**  
   Chunks are embedded using a local Ollama embedding model (`all-minilm:22m`) for efficient semantic search.

3. **Retrieval**  
   User queries are embedded and matched against stored chunks via cosine similarity. Only chunks exceeding a relevance threshold (0.65) are used; otherwise, the system declines to answer.

4. **Generation**  
   The local Ollama LLM (`qwen2.5:7b-instruct`) generates answers strictly based on retrieved context, avoiding hallucination.

5. **Citation**  
   Responses include source metadata (file name, heading, and line range) for transparency.

---

## Key Features

- **Fully Local & Private:** No data leaves your environment.  
- **RAG with Verified Sources:** Answers are grounded and auditable.  
- **Persistent Vector Store:** Uses ChromaDB to store embeddings locally (`./chroma_data`).  
- **Automatic KB Sync:** Updates only new or modified files on startup.  
- **Relevance Filtering:** Uses cosine similarity to ensure answer quality.  
- **Powered by Ollama:** Local LLM and embedding models ensure fast, reliable inference.

---

## Prerequisites

- Docker & Docker Compose installed  
- Ollama instance running locally or accessible on network (e.g., `OLLAMA_HOST=0.0.0.0`)  
- Required Ollama models pulled locally:  

```sh
ollama pull qwen2.5:7b-instruct
ollama pull all-minilm:22m
  ```

## Quickstart

1.  **Clone the repository** (if you haven't already).

2.  **Configure the Environment**: Copy the example environment file.
    ```sh
    cp .env.example .env
    ```
    Open the `.env` file and edit the `OLLAMA_BASE_URL` to point to the IP address of your machine running Ollama. **Do not use `localhost` or `127.0.0.1`** unless Ollama is running on the same machine where you are running the `docker compose` command. A common value is `http://host.docker.internal:11434`, which allows the container to connect back to the host machine.

3.  **Build and Run the Service**:
    ```sh
    docker compose up --build
    ```
    The `-d` flag can be added to run the container in detached mode.

4.  **Access the Chatbot**: Open your web browser and navigate to `http://localhost:8000`.

## Testing from the Command Line

You can also test the API endpoints directly using `curl`.

### Health Check

This endpoint confirms that the service is running and shows the configured Ollama models.

```sh
curl -s http://localhost:8000/health | jq .
```
*Expected Output:*
```json
{
  "status": "ok",
  "ollama_base_url": "http://host.docker.internal:11434",
  "ollama_llm_model": "qwen2.5:7b-instruct",
  "ollama_embed_model": "all-minilm:22m"
}
```

### Chat Endpoint

Send a question to the chatbot.

```sh
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"What is this project for?"}' | jq .
```
*Expected Output:*
```json
{
  "answer": "This project aims to create a simple, self-contained FAQ chatbot that runs on a local VM using Docker Compose and connects to a local Ollama instance for large language model inference.",
  "sources": [
    {
      "file": "01-project-goal.md",
      "heading": "Project Goal",
      "start_line": 1,
      "end_line": 3
    }
  ]
}
```

## Troubleshooting

### Cannot Connect to Ollama

This is the most common issue. If the application logs show errors like `Connection refused` or timeouts when trying to reach Ollama:

- **Wrong IP Address**: Double-check the `OLLAMA_BASE_URL` in your `.env` file. It must be the LAN IP of your Ollama machine, or `host.docker.internal` if running Docker Desktop.
- **Ollama Not Bound to LAN**: Make sure your Ollama instance is configured to accept connections from other machines. You typically do this by setting the `OLLAMA_HOST=0.0.0.0` environment variable for the Ollama service.
- **Firewall**: A firewall on the machine running Ollama might be blocking port `11434`.

### Port Conflict

If `docker compose up` fails with an error about a port being in use, it means another service is already using port `8000` on your machine. You can change the port mapping in `docker-compose.yml` from `"8000:8000"` to something else, like `"8001:8000"`.
