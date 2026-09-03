"""
Retriever component for semantic document search and context fetching.
"""

import math
import re
from typing import List, Dict, Any


def compute_term_overlap_score(query: str, text: str) -> float:
    """Computes a normalized overlap score between query tokens and document text."""
    query_tokens = set(re.findall(r'\w+', query.lower()))
    text_tokens = re.findall(r'\w+', text.lower())
    if not query_tokens or not text_tokens:
        return 0.0

    matches = sum(1 for token in text_tokens if token in query_tokens)
    # Length-dampened BM25-like scoring
    tf = matches / (len(text_tokens) + 10)
    return tf * 10.0


class RAGRetriever:
    """Retrieves relevant document chunks with source attribution and scoring."""

    def __init__(self, documents: List[Dict[str, Any]]):
        self.documents = documents

    def retrieve(self, query: str, top_k: int = 3, min_score: float = 0.05) -> List[Dict[str, Any]]:
        """
        Retrieves top_k most relevant chunks for a user query.
        """
        scored_docs = []
        for doc in self.documents:
            score = compute_term_overlap_score(query, doc["content"])
            scored_docs.append({
                **doc,
                "score": round(score, 4)
            })

        # Sort by relevance score descending
        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        results = [doc for doc in scored_docs if doc["score"] >= min_score][:top_k]

        # If strict term overlap yields 0 results, return top documents with non-zero fallback
        if not results and scored_docs:
            results = scored_docs[:top_k]

        return results
