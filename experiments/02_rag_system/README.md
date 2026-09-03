# Module 02: Enterprise RAG-Based Question Answering System

## Overview
This module implements a production-grade Retrieval-Augmented Generation (RAG) system. It features document chunking with character overlap, vector index persistence, similarity retrieval, and strict ground-truth prompt formatting to prevent model hallucination while surfacing verifiable source citations.

## Architecture
```
Enterprise Raw Documents (.txt, .md, .pdf)
                   │
                   ▼
  [Recursive Text Splitter & Chunker]
                   │
                   ▼
    [Vector Indexing & Embedding Engine]
                   │
                   ▼
 User Query ──► [Semantic Retriever]
                   │
         Top-K Context Chunks
                   │
                   ▼
       [Grounded Prompt Assembly]
                   │
                   ▼
         [LLM Synthesis Engine]
                   │
                   ▼
Answer with Source Citations & Scores
```

## Quickstart Usage
```python
from experiments.02_rag_system.qa_chain import RAGSystem

rag = RAGSystem()
response = rag.query("What are the enterprise security rules regarding PII?")

print("Answer:\n", response["answer"])
print("\nSources used:", [s["source"] for s in response["sources"]])
```
