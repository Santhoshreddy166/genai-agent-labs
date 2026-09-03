# Module 01: Enterprise Text-to-SQL Workflow

## Overview
This module demonstrates an enterprise-grade natural language to SQL translation pipeline. The system couples schema introspection with an automated self-correction loop and AST-based security guardrails to ensure generated queries are syntactically sound and non-destructive.

## Architecture
```
User Natural Language Question
           │
           ▼
[Dynamic Schema Introspection] ───► Injects table definitions & foreign keys
           │
           ▼
   [LLM SQL Generator]
           │
           ▼
 [SQL AST & Safety Validator]
     ├── Destructive Check (DROP, DELETE, UPDATE, ALTER) ──► Block & Alarm
     └── Syntax & Schema Check (EXPLAIN sqlite execution)
           │
     ┌─────┴─────────────────────────┐
  [Passed]                        [Failed]
     │                               │
     ▼                               ▼
[Safe Execution]           [Feedback Loop to LLM]
     │                    (Self-Correction Prompt)
     ▼                               │
Output Data Table                    └──► Retries (up to 3x)
```

## Key Files
- `pipeline.py`: Orchestrates the prompt generation, extraction, retry loop, and execution.
- `schema_validator.py`: Provides read-only AST safety validation and SQLite `EXPLAIN` syntax verification.

## Quickstart Usage
```python
from experiments.01_text_to_sql.pipeline import TextToSQLPipeline

pipeline = TextToSQLPipeline(max_retries=3)
result = pipeline.generate_sql("Who are the top 3 customers by total spending?")

print(f"Generated SQL: {result['sql']}")
print(f"Status: {result['status']}")
print(f"Result Rows: {result['execution']['rows']}")
```
