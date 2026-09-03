"""
End-to-end Text-to-SQL pipeline with schema grounding and self-correction.
"""

import re
from typing import Dict, Any, List
from src.utils import get_llm, get_schema_summary, execute_sql_safely
from src.config import use_mock
from .schema_validator import SchemaValidator


SYSTEM_PROMPT = """You are an expert SQL Data Architect specializing in SQLite.
Given the database schema below, translate the user's natural language question into a clean, safe, valid SQLite query.

Schema:
{schema}

Instructions:
1. Return ONLY the executable SQL query. Do not wrap in conversational text.
2. Use standard SQLite syntax and functions.
3. Only write SELECT statements. Mutating commands (DROP, DELETE, UPDATE, INSERT) are strictly forbidden.
4. Use clear aliases and limit result sets to 20 rows unless explicitly specified otherwise.
"""

CORRECTION_PROMPT = """The previously generated SQL query failed schema/syntax validation.
Original Question: {question}
Failed Query: {query}
Validation Error: {error}

Database Schema:
{schema}

Please analyze the error and provide a corrected, valid SQLite SELECT query. Return ONLY the SQL query.
"""


class TextToSQLPipeline:
    def __init__(self, max_retries: int = 3):
        self.llm = get_llm()
        self.validator = SchemaValidator()
        self.max_retries = max_retries

    def _extract_sql(self, text: str) -> str:
        """Strip markdown fences and whitespace from LLM response."""
        clean = text.strip()
        # Look for ```sql ... ```
        match = re.search(r'```(?:sql)?(.*?)```', clean, re.DOTALL | re.IGNORECASE)
        if match:
            clean = match.group(1).strip()
        return clean.strip("`").strip()

    def generate_sql(self, user_question: str) -> Dict[str, Any]:
        """
        Executes NL -> SQL translation with a self-correction loop.
        """
        schema = get_schema_summary()
        prompt = SYSTEM_PROMPT.format(schema=schema) + f"\nUser Question: {user_question}\nSQL Query:"

        history: List[Dict[str, str]] = []
        current_query = ""

        for attempt in range(self.max_retries + 1):
            if attempt == 0:
                raw_response = self.llm.invoke(prompt)
            else:
                retry_prompt = CORRECTION_PROMPT.format(
                    question=user_question,
                    query=current_query,
                    error=history[-1]["error"],
                    schema=schema
                )
                raw_response = self.llm.invoke(retry_prompt)

            content = getattr(raw_response, "content", str(raw_response))
            current_query = self._extract_sql(content)

            # Validate query
            is_valid, error = self.validator.validate_syntax_and_schema(current_query)

            if is_valid:
                # Execute query safely
                exec_result = execute_sql_safely(current_query)
                return {
                    "question": user_question,
                    "sql": current_query,
                    "attempts": attempt + 1,
                    "correction_history": history,
                    "execution": exec_result,
                    "status": "SUCCESS" if exec_result["success"] else "EXECUTION_ERROR"
                }
            else:
                history.append({
                    "attempt": attempt + 1,
                    "query": current_query,
                    "error": error or "Unknown validation error"
                })

        return {
            "question": user_question,
            "sql": current_query,
            "attempts": self.max_retries + 1,
            "correction_history": history,
            "execution": {"success": False, "error": "Max correction retries exceeded.", "rows": [], "columns": []},
            "status": "VALIDATION_FAILED"
        }
