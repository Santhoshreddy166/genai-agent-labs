"""
End-to-end RAG QA Chain with grounded context synthesis and citation tracking.
"""

from typing import Dict, Any, List
from src.utils import get_llm
from src.config import use_mock
from .ingest import VectorIndexManager
from .retriever import RAGRetriever

RAG_PROMPT_TEMPLATE = """You are an Enterprise Knowledge Assistant.
Answer the question strictly based on the retrieved context passages below.
If the context does not contain sufficient information, state:
"Based on the provided enterprise documentation, I do not have enough verified context to answer this question."

Context Passages:
{context}

Question: {question}

Response format:
- Clear, factual answer grounded in the text.
- Explicit section titled "Sources & Citations" referencing the document name and chunk index.
"""


class RAGSystem:
    def __init__(self):
        self.index_manager = VectorIndexManager()
        self.index_manager.ingest_directory()
        self.retriever = RAGRetriever(self.index_manager.get_documents())
        self.llm = get_llm()

    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Executes the RAG pipeline: retrieval -> prompt synthesis -> citation-backed answer.
        """
        retrieved_chunks = self.retriever.retrieve(question, top_k=top_k)

        # Build context string
        context_blocks = []
        sources = []
        for chunk in retrieved_chunks:
            source_tag = f"[{chunk['source']} - Chunk #{chunk['chunk_index']}]"
            context_blocks.append(f"{source_tag}:\n{chunk['content']}")
            sources.append({
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
                "score": chunk.get("score", 0.0),
                "snippet": chunk["content"][:160] + "..."
            })

        context_str = "\n\n---\n\n".join(context_blocks)
        prompt = RAG_PROMPT_TEMPLATE.format(context=context_str, question=question)

        if use_mock():
            answer = (
                f"Based on the enterprise architecture and security policies, "
                f"agentic systems require strict execution boundaries (e.g. read-only database connections) "
                f"and automated PII sanitization before prompt transmission.\n\n"
                f"### Sources & Citations:\n"
                f"- `agentic_workflows_overview.txt` (Chunk #0)\n"
                f"- `enterprise_security_policy.txt` (Chunk #0)"
            )
        else:
            response = self.llm.invoke(prompt)
            answer = getattr(response, "content", str(response))

        return {
            "question": question,
            "answer": answer,
            "retrieved_context": retrieved_chunks,
            "sources": sources,
            "chunks_used": len(retrieved_chunks)
        }
