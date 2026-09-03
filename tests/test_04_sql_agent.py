"""
Unit tests for Module 04: SQL ReAct Agent
"""

import pytest
from experiments import (
    check_sql_safety,
    tool_list_tables,
    tool_describe_schema,
    SQLReActAgent
)


def test_guardrails_destructive_check():
    is_safe, err = check_sql_safety("DROP TABLE customers;")
    assert is_safe is False
    assert "DROP" in err

    is_safe2, err2 = check_sql_safety("SELECT * FROM customers;")
    assert is_safe2 is True
    assert err2 is None


def test_tool_list_tables():
    res = tool_list_tables()
    assert "customers" in res
    assert "orders" in res


def test_react_agent_destructive_intercept():
    agent = SQLReActAgent()
    result = agent.run("DROP TABLE customers;")
    assert result["status"] == "BLOCKED_BY_GUARDRAIL"
    assert "Refused" in result["final_answer"]
