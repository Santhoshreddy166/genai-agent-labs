"""
Tool definitions for the SQL ReAct agent.
"""

import json
from typing import Dict, Any
from src.utils import get_schema_summary, get_db_connection, execute_sql_safely
from .guardrails import check_sql_safety


def tool_list_tables() -> str:
    """Lists all user tables available in the enterprise SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return json.dumps({"available_tables": tables})


def tool_describe_schema(table_name: str = "") -> str:
    """Returns column names and types for all tables or a specific table."""
    full_schema = get_schema_summary()
    if not table_name:
        return full_schema
    
    # Filter for table
    sections = full_schema.split("\n\n")
    for sec in sections:
        if f"Table: {table_name}" in sec:
            return sec
    return f"Table '{table_name}' not found in database."


def tool_run_sql(query: str) -> str:
    """Safely executes a read-only SQL query against the database."""
    is_safe, error = check_sql_safety(query)
    if not is_safe:
        return json.dumps({"error": error, "status": "GUARDRAIL_BLOCKED"})

    result = execute_sql_safely(query)
    if not result["success"]:
        return json.dumps({"error": result["error"], "status": "QUERY_ERROR"})

    return json.dumps({
        "status": "SUCCESS",
        "row_count": result["row_count"],
        "rows": result["rows"][:10]  # Cap at 10 rows for context brevity
    }, default=str)
