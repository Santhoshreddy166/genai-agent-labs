"""
Schema validation and guardrail checks for generated SQL queries.
"""

import re
from typing import Tuple, List, Optional
try:
    import sqlparse
except ImportError:
    sqlparse = None

from src.utils import get_db_connection

FORBIDDEN_KEYWORDS = [
    "DROP", "DELETE", "TRUNCATE", "UPDATE", "INSERT", 
    "ALTER", "CREATE", "REPLACE", "GRANT", "REVOKE"
]


class SchemaValidator:
    """Validates SQL query syntax, permissions, and table/column references."""

    @staticmethod
    def is_safe_read_only(query: str) -> Tuple[bool, Optional[str]]:
        """Verify that the query contains only read-only statements."""
        clean = query.strip()
        if not clean:
            return False, "Empty query."

        for word in FORBIDDEN_KEYWORDS:
            if re.search(r'\b' + word + r'\b', clean, re.IGNORECASE):
                return False, f"Security Violation: Destructive command '{word}' is forbidden."

        if sqlparse:
            parsed = sqlparse.parse(clean)
            if not parsed:
                return False, "Empty or unparseable query."

            for statement in parsed:
                stmt_type = statement.get_type()
                if stmt_type != "SELECT":
                    return False, f"Non-SELECT statement type '{stmt_type}' detected. Only read-only queries are permitted."
        else:
            first_word = clean.split()[0].upper()
            if first_word not in ("SELECT", "WITH", "EXPLAIN", "PRAGMA"):
                return False, f"Only read-only queries starting with SELECT/WITH are permitted. Got: '{first_word}'."

        return True, None

    @staticmethod
    def validate_syntax_and_schema(query: str) -> Tuple[bool, Optional[str]]:
        """
        Executes an EXPLAIN query in SQLite to validate syntax and table/column existence
        without executing the underlying query.
        """
        is_safe, error = SchemaValidator.is_safe_read_only(query)
        if not is_safe:
            return False, error

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"EXPLAIN {query}")
            conn.close()
            return True, None
        except Exception as e:
            return False, f"SQLite Syntax/Schema Error: {str(e)}"
