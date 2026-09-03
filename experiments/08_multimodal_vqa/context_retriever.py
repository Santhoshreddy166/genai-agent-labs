"""
Context retriever for multimodal visual QA augmentation.
"""

from typing import List, Dict, Any
from experiments import VectorIndexManager, RAGRetriever


class MultimodalContextRetriever:
    """Fetches textual context to ground visual inquiries."""

    def __init__(self):
        index = VectorIndexManager()
        index.ingest_directory()
        self.retriever = RAGRetriever(index.get_documents())

    def get_context_for_query(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        return self.retriever.retrieve(query, top_k=top_k)
