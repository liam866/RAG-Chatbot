# Local RAG FAQ Chatbot

A self-contained FAQ chatbot designed to run locally via Docker Compose. It connects to a local Ollama instance to perform retrieval-augmented generation (RAG) over a Markdown-based knowledge base.

## Key Features

- **Fully Local & Private**: All components run within your environment. No data is transmitted outside your network.
- **Retrieval-Augmented Generation (RAG)**: Answers are grounded in your documentation, reducing hallucinations and providing clear, verifiable source citations.
- **Ollama Powered**: Integrates with local Ollama models for both embedding (all-minilm:22m) and generation (qwen2.5:7b-instruct).
- **Persistent Vector Store**: Uses ChromaDB for efficient, persistent storage of embeddings, with data stored locally in the ./chroma_data directory.
- **Automatic Synchronization**: Automatically synchronizes the vector store with the /kb directory on startup, processing only new or modified files.
- **Relevance Filtering**: Applies cosine similarity with a distance threshold to ensure only relevant documents are used when generating responses.

## How It Works

The application follows a standard RAG pipeline:

1. **Sync KB**: On startup, the backend parses .md files from the /kb directory, chunks the content, hashes each chunk, and synchronizes additions, updates, or deletions with the ChromaDB vector store.
2. **Embed**: New or updated chunks are converted into vector embeddings using the local Ollama embedding model.
3. **Retrieve**: A user query is embedded and used to retrieve the most similar document chunks from ChromaDB via cosine similarity search. Chunks that do not meet the relevance threshold are discarded.
4. **Generate**: The retrieved context and original question are passed to the local LLM, which generates a response strictly constrained to the provided content.
5. **Cite**: The final response includes metadata (file name, section heading, and line range) corresponding to the source material.

## Prerequisites

- **Docker and Docker Compose**: Docker and Docker Compose must be installed on your system.
- **Ollama**: A running Ollama instance accessible from Docker containers. Ollama should be configured to listen on a network address (e.g. OLLAMA_HOST=0.0.0.0).
- **Ollama Models**: The required models must be available locally. Pull them using:

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
