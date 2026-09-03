"""
Safety guardrails for SQL execution tools.
Intercepts and prevents destructive statements before reaching the database engine.
"""

import re
from typing import Tuple, Optional


class SQLGuardrailError(Exception):
    """Raised when a query violates safety constraints."""
    pass


FORBIDDEN_OPERATIONS = [
    r'\bDROP\b',
    r'\bDELETE\b',
    r'\bTRUNCATE\b',
    r'\bALTER\b',
    r'\bUPDATE\b',
    r'\bINSERT\b',
    r'\bGRANT\b',
    r'\bREVOKE\b',
    r'\bATTACH\b',
    r'\bDETACH\b'
]


def check_sql_safety(query: str) -> Tuple[bool, Optional[str]]:
    """
    Verifies that a query is strictly read-only.
    Returns (True, None) if safe, or (False, error_message) if violated.
    """
    clean_query = query.strip()
    
    if not clean_query:
        return False, "Query is empty."

    for pattern in FORBIDDEN_OPERATIONS:
        match = re.search(pattern, clean_query, re.IGNORECASE)
        if match:
            forbidden_word = match.group(0).upper()
            return False, f"SECURITY ALERT: Destructive SQL keyword '{forbidden_word}' is forbidden."

    # Must start with SELECT or EXPLAIN or PRAGMA table_info
    first_word = clean_query.split()[0].upper()
    if first_word not in ("SELECT", "EXPLAIN", "PRAGMA", "WITH"):
        return False, f"SECURITY ALERT: Queries must begin with SELECT, WITH, or PRAGMA. Got: '{first_word}'."

    return True, None
