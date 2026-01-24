from typing import List, Tuple
from .schemas import DocumentChunk
from .vector_store import VectorStore

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def search(self, query: str, top_k: int) -> List[DocumentChunk]:
        """
        Performs a search using the vector store, applying the relevance threshold.
        """
        return self.vector_store.query(query_text=query, n_results=top_k)

    def retrieve_for_debug(self, query: str, top_k: int) -> List[Tuple[DocumentChunk, float]]:
        """
        Retrieves chunks with their distances, without applying the relevance threshold.
        This is for debugging and inspection purposes.
        """
        return self.vector_store.retrieve_with_distances(query_text=query, n_results=top_k)
