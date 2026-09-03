"""
Document ingestion, text chunking, and vector indexing pipeline.
"""

from pathlib import Path
from typing import List, Dict, Any
from src.config import DOCS_DIR, CHROMA_PERSIST_DIR
from src.utils import get_embeddings, logger


class SimpleTextChunker:
    """Lightweight deterministic chunker with character and overlap handling."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunks.append(text[start:end].strip())
            if end == text_len:
                break
            start += self.chunk_size - self.chunk_overlap

        return [c for c in chunks if c]


class VectorIndexManager:
    """Manages document chunking and vector storage."""

    def __init__(self, persist_dir: Path = CHROMA_PERSIST_DIR):
        self.persist_dir = persist_dir
        self.chunker = SimpleTextChunker()
        self.embeddings = get_embeddings()
        self._in_memory_docs: List[Dict[str, Any]] = []

    def ingest_directory(self, directory: Path = DOCS_DIR) -> int:
        """Loads all .txt and .md documents from directory into the vector store."""
        total_chunks = 0
        if not directory.exists():
            logger.warning(f"Docs directory {directory} not found.")
            return 0

        files = list(directory.glob("*.txt")) + list(directory.glob("*.md"))
        for file_path in files:
            content = file_path.read_text(encoding="utf-8")
            chunks = self.chunker.split_text(content)
            for idx, chunk in enumerate(chunks):
                self._in_memory_docs.append({
                    "id": f"{file_path.stem}_{idx}",
                    "source": file_path.name,
                    "chunk_index": idx,
                    "content": chunk,
                })
                total_chunks += 1

        logger.info(f"Ingested {len(files)} files into {total_chunks} chunks.")
        return total_chunks

    def get_documents(self) -> List[Dict[str, Any]]:
        return self._in_memory_docs
