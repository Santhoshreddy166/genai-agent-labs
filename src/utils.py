"""
Core utility module for AI Labs.
Provides LLM factories, mock fallbacks, database connectors, and logging tools.
"""

import os
import re
import json
import logging
import sqlite3
from typing import Any, Dict, List, Optional

from src.config import (
    SQLITE_DB_PATH,
    LLM_PROVIDER,
    DEFAULT_MODEL,
    TEMPERATURE,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    GOOGLE_API_KEY,
    use_mock
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ai-labs")


# ==============================================================================
# 1. Mock LLM for Offline / Demonstration Mode
# ==============================================================================
class MockChatModel:
    """Deterministic simulated LLM for testing without API keys."""
    
    def __init__(self, model_name: str = "mock-gpt-4o"):
        self.model_name = model_name

    def invoke(self, prompt: Any) -> Any:
        prompt_text = str(prompt)
        
        # SQL extraction mock
        if "SQL" in prompt_text or "SELECT" in prompt_text:
            return MockMessage(
                "SELECT c.name, COUNT(o.id) AS total_orders, SUM(o.total_amount) AS total_spent "
                "FROM customers c "
                "JOIN orders o ON c.id = o.customer_id "
                "GROUP BY c.id "
                "ORDER BY total_spent DESC LIMIT 5;"
            )
        # Summarization / Key points mock
        elif "summarize" in prompt_text.lower() or "key points" in prompt_text.lower():
            return MockMessage(
                "### Key Points:\n"
                "1. Rapid expansion in generative AI adoption across enterprise verticals.\n"
                "2. Implementation of agentic workflows yields 45% productivity gains.\n"
                "3. Robust policy guardrails and schema validation are critical for production."
            )
        # SDR Multi-Agent mock
        elif "lead" in prompt_text.lower() or "prospect" in prompt_text.lower():
            return MockMessage(
                json.dumps({
                    "name": "Sarah Jenkins",
                    "title": "VP of Engineering",
                    "company": "CloudScale Systems",
                    "icp_score": 92,
                    "rationale": "High tech stack synergy, expanding AI engineering headcount.",
                    "personalized_hook": "Saw your recent post on scaling RAG retrieval pipelines."
                }, indent=2)
            )
        # Policy compliance mock
        elif "compliance" in prompt_text.lower() or "policy" in prompt_text.lower():
            return MockMessage(
                json.dumps({
                    "status": "FLAGGED",
                    "risk_score": 78,
                    "violations": [
                        "Direct exposure of customer email and credit card snippet (PCI/PII violation)",
                        "Promissory language regarding guaranteed investment yields"
                    ],
                    "recommendations": "Sanitize customer identifiers using masking tokens [PII_REDACTED]."
                }, indent=2)
            )
        # Default mock response
        return MockMessage(
            f"Simulated response from {self.model_name}. System functioning normally in mock mode. "
            f"Input preview: {prompt_text[:120]}..."
        )

    def __call__(self, prompt: Any) -> Any:
        return self.invoke(prompt)


class MockMessage:
    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content


# ==============================================================================
# 2. LLM and Embeddings Factory
# ==============================================================================
def get_llm(model: Optional[str] = None, temperature: float = TEMPERATURE):
    """
    Factory function to retrieve a LangChain LLM instance.
    Falls back gracefully to MockChatModel if no valid credentials exist.
    """
    selected_model = model or DEFAULT_MODEL

    if use_mock():
        logger.info(f"Operating in MOCK_MODE. Using MockChatModel ({selected_model}).")
        return MockChatModel(model_name=selected_model)

    try:
        if LLM_PROVIDER == "openai" and OPENAI_API_KEY:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=selected_model,
                temperature=temperature,
                api_key=OPENAI_API_KEY
            )
        elif LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY:
            from langchain_community.chat_models import ChatAnthropic
            return ChatAnthropic(
                model=selected_model,
                temperature=temperature,
                anthropic_api_key=ANTHROPIC_API_KEY
            )
        else:
            logger.warning("Configured provider missing key. Defaulting to MockChatModel.")
            return MockChatModel(model_name=selected_model)
    except Exception as e:
        logger.error(f"Failed to initialize LLM provider: {e}. Falling back to MockChatModel.")
        return MockChatModel(model_name=selected_model)


class MockEmbeddings:
    """Mock embeddings for offline environments."""
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [[0.05 * (i % 10) for i in range(128)] for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        return [0.05 * (i % 10) for i in range(128)]


def get_embeddings():
    """Factory for text embeddings."""
    if use_mock():
        return MockEmbeddings()

    try:
        if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-proj-your"):
            from langchain_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    except Exception as e:
        logger.warning(f"Could not load OpenAI embeddings: {e}. Using MockEmbeddings.")
    return MockEmbeddings()


# ==============================================================================
# 3. Database Engine & Inspection Utilities
# ==============================================================================
def get_db_engine():
    """Create and return an SQLAlchemy engine for the demo database if available."""
    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db_uri = f"sqlite:///{SQLITE_DB_PATH.as_posix()}"
    try:
        from sqlalchemy import create_engine
        return create_engine(db_uri, echo=False)
    except ImportError:
        return None


def get_db_connection() -> sqlite3.Connection:
    """Return raw sqlite3 connection."""
    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(SQLITE_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def get_schema_summary() -> str:
    """
    Introspects the SQLite database and returns a human-readable schema string
    suitable for feeding into prompt contexts. Uses sqlite3 directly for zero dependencies.
    """
    if not SQLITE_DB_PATH.exists():
        return "Database not initialized. Please run data/seed_data.py first."

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    schema_lines = []
    for table_name in tables:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        col_strs = [f"{col['name']} ({col['type']})" for col in columns]
        schema_lines.append(f"Table: {table_name}\n  Columns: {', '.join(col_strs)}")

    conn.close()
    return "\n\n".join(schema_lines)


def execute_sql_safely(query: str) -> Dict[str, Any]:
    """
    Executes a read-only SQL query safely with guardrails against mutating queries.
    """
    # Guardrail check
    forbidden = ["drop", "delete", "truncate", "update", "insert", "alter", "create", "replace"]
    clean_query = query.strip().lower()
    for word in forbidden:
        # Match whole word
        if re.search(r'\b' + word + r'\b', clean_query):
            return {
                "success": False,
                "error": f"Security Guardrail Violation: Destructive operation '{word.upper()}' is not permitted.",
                "rows": [],
                "columns": []
            }

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return {
            "success": True,
            "error": None,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "columns": [],
            "rows": []
        }
