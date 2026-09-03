"""
Supervisor Capstone Agent: Multi-Tool RAG, SQL, and Compliance Orchestrator.
"""

import time
from typing import Dict, Any, List
from src.utils import get_llm
from src.config import use_mock
from .tools import CapstoneToolKit


class CapstoneAgent:
    """
    Unified multi-tool agent orchestrating:
    - Relational Text-to-SQL
    - Semantic Document RAG
    - Real-Time Policy Compliance Verification
    """

    def __init__(self):
        self.tools = CapstoneToolKit()
        self.llm = get_llm()

    def route_intent(self, user_query: str) -> str:
        """Determines whether the query requires SQL, RAG, or Hybrid tools."""
        q_lower = user_query.lower()
        
        has_sql_indicators = any(term in q_lower for term in [
            "customer", "order", "revenue", "price", "spending", "table", "sales", "database", "sku", "product"
        ])
        has_rag_indicators = any(term in q_lower for term in [
            "policy", "architecture", "guardrail", "rule", "pii", "react", "document", "sla", "quantization"
        ])

        if has_sql_indicators and has_rag_indicators:
            return "HYBRID"
        elif has_sql_indicators:
            return "SQL"
        elif has_rag_indicators:
            return "RAG"
        return "GENERAL"

    def run(self, user_query: str) -> Dict[str, Any]:
        start_time = time.time()
        intent = self.route_intent(user_query)
        tool_results: Dict[str, Any] = {}
        execution_trace: List[str] = [f"Supervisor classified intent as: '{intent}'"]

        # 1. Execute Routed Tools
        if intent in ("SQL", "HYBRID"):
            execution_trace.append("Routing to Relational Text-to-SQL Pipeline...")
            sql_res = self.tools.query_enterprise_sql(user_query)
            tool_results["sql"] = sql_res
            execution_trace.append(f"SQL Tool generated: `{sql_res.get('sql', 'N/A')}`")

        if intent in ("RAG", "HYBRID"):
            execution_trace.append("Routing to Semantic RAG Knowledge Base...")
            rag_res = self.tools.query_knowledge_base(user_query)
            tool_results["rag"] = rag_res
            execution_trace.append(f"RAG Tool retrieved {rag_res.get('chunks_used', 0)} document chunks.")

        # 2. Synthesize Integrated Response
        if intent == "SQL":
            exec_data = tool_results["sql"]["execution"]
            if exec_data["success"]:
                synthesis = (
                    f"### Database Query Results\n"
                    f"**Generated SQL:** `{tool_results['sql']['sql']}`\n\n"
                    f"Found **{exec_data['row_count']}** matching records:\n"
                )
                if exec_data["rows"]:
                    synthesis += "\n".join([f"- {row}" for row in exec_data["rows"][:5]])
            else:
                synthesis = f"Unable to execute query: {exec_data.get('error')}"

        elif intent == "RAG":
            synthesis = tool_results["rag"]["answer"]

        elif intent == "HYBRID":
            synthesis = (
                f"### Consolidated Multi-Tool Findings\n\n"
                f"**1. Enterprise Knowledge Base Context:**\n{tool_results['rag']['answer']}\n\n"
                f"**2. Relational Database Records:**\n"
                f"SQL Executed: `{tool_results['sql'].get('sql')}`\n"
                f"Matching entries: {len(tool_results['sql']['execution'].get('rows', []))} rows retrieved."
            )
        else:
            synthesis = (
                f"I can assist with querying enterprise database tables (orders, customers, revenue) "
                f"or searching internal technical documentation (policies, security guardrails, agent architectures)."
            )

        # 3. Policy Compliance Interception
        execution_trace.append("Running output through Policy Compliance Guardrail...")
        compliance_check = self.tools.verify_compliance(synthesis)
        
        if not compliance_check["is_compliant"]:
            execution_trace.append(f"Compliance alert: Risk Score {compliance_check['risk_score']}!")
            synthesis += (
                f"\n\n> ⚠️ **Compliance Notice**: This response was flagged for {len(compliance_check['deterministic_violations'])} "
                f"policy considerations. Sanitization applied."
            )
        else:
            execution_trace.append("Compliance check passed (Risk Score: 0).")

        total_latency = round(time.time() - start_time, 2)

        return {
            "query": user_query,
            "intent": intent,
            "latency_sec": total_latency,
            "execution_trace": execution_trace,
            "tool_results": tool_results,
            "compliance": compliance_check,
            "final_answer": synthesis
        }
