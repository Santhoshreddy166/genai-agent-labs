"""
Unified tool suite for Capstone Multi-Tool Agent.
Integrates RAG retrieval, safe SQL execution, and policy compliance verification.
"""

from typing import Dict, Any
from experiments import (
    TextToSQLPipeline,
    RAGSystem,
    PolicyComplianceAgent
)


class CapstoneToolKit:
    """Provides a consolidated suite of enterprise tools."""

    def __init__(self):
        self.sql_pipeline = TextToSQLPipeline()
        self.rag_system = RAGSystem()
        self.policy_agent = PolicyComplianceAgent()

    def query_enterprise_sql(self, natural_language_question: str) -> Dict[str, Any]:
        """Queries the enterprise relational database (customers, products, orders, sales reps)."""
        return self.sql_pipeline.generate_sql(natural_language_question)

    def query_knowledge_base(self, question: str) -> Dict[str, Any]:
        """Retrieves verified context from internal architecture and policy documents."""
        return self.rag_system.query(question)

    def verify_compliance(self, text: str) -> Dict[str, Any]:
        """Scans any text for regulatory, PII, and financial policy violations."""
        return self.policy_agent.evaluate(text)
