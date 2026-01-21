# Project Goal

This project aims to create a simple, self-contained FAQ chatbot.

## Key Features

- **Local First**: It runs on a local VM using Docker Compose.
- **Ollama Integration**: It connects to a local Ollama instance for large language model (LLM) inference.
- **RAG**: It uses a Retrieval-Augmented Generation (RAG) approach, grounding its answers in a local knowledge base of Markdown files.
- **Citations**: The chatbot provides citations for its answers, pointing to the specific file, heading, and line numbers it used as a source.

## Technology Stack

- **Backend**: Python with FastAPI
- **LLM**: Ollama (specifically the `qwen2.5:7b-instruct` model)
- **Containerization**: Docker Compose
