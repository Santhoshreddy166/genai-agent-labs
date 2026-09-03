"""
Unit tests for Module 02: RAG-Based Question Answering System
"""

import pytest
from experiments import (
    SimpleTextChunker,
    VectorIndexManager,
    RAGRetriever,
    compute_term_overlap_score,
    RAGSystem
)


def test_chunker_basic():
    chunker = SimpleTextChunker(chunk_size=100, chunk_overlap=20)
    sample_text = "Word " * 50
    chunks = chunker.split_text(sample_text)
    assert len(chunks) > 1
    assert all(len(c) <= 120 for c in chunks)


def test_term_overlap_scoring():
    query = "database security guardrail"
    text_matching = "The database security guardrail prevents destructive operations."
    text_unrelated = "Strawberries are bright red summer fruits."

    score_high = compute_term_overlap_score(query, text_matching)
    score_low = compute_term_overlap_score(query, text_unrelated)

    assert score_high > score_low
    assert score_low == 0.0


def test_rag_system_query():
    rag = RAGSystem()
    result = rag.query("What are the security guidelines for handling PII?")
    assert "answer" in result
    assert "sources" in result
    assert len(result["sources"]) > 0
