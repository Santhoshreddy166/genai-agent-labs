"""
Unit tests for Module 01: Text-to-SQL Workflow
"""

import pytest
from experiments import SchemaValidator, TextToSQLPipeline


def test_schema_validator_read_only_success():
    query = "SELECT id, name, email FROM customers WHERE tier = 'Enterprise';"
    is_safe, error = SchemaValidator.is_safe_read_only(query)
    assert is_safe is True
    assert error is None


def test_schema_validator_destructive_drop_blocked():
    query = "DROP TABLE customers;"
    is_safe, error = SchemaValidator.is_safe_read_only(query)
    assert is_safe is False
    assert "forbidden" in error.lower() or "destructive" in error.lower()


def test_schema_validator_destructive_delete_blocked():
    query = "DELETE FROM orders WHERE id = 1;"
    is_safe, error = SchemaValidator.is_safe_read_only(query)
    assert is_safe is False


def test_text_to_sql_pipeline_execution():
    pipeline = TextToSQLPipeline(max_retries=1)
    result = pipeline.generate_sql("List 3 customers.")
    assert "sql" in result
    assert result["attempts"] >= 1
    assert "execution" in result
