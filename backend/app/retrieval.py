from typing import List
from .schemas import DocumentChunk
from .vector_store import VectorStore

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def search(self, query: str, top_k: int) -> List[DocumentChunk]:

        return self.vector_store.query(query_text=query, n_results=top_k)
