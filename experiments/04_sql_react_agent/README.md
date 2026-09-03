# Module 04: SQL Agent with Tool Use (ReAct Architecture)

## Overview
This module demonstrates an autonomous database agent powered by the **ReAct (Reason + Act)** framework. Rather than guessing an answer in one shot, the agent cycles through *Thought*, *Action*, and *Observation* steps, utilizing tools to inspect schemas and run analytical queries while adhering to strict safety guardrails.

## Safety Guardrails
The agent is wrapped with AST and token-level safety checks:
- Blocks queries with destructive keywords (`DROP`, `DELETE`, `TRUNCATE`, `ALTER`, `UPDATE`, `INSERT`).
- Enforces read-only statements (`SELECT`, `WITH`, `PRAGMA`).
- Restricts row exposure to prevent token context explosion.

## Step-by-Step Flow
```
User Query: "Which enterprise customer spent the most?"
  │
  ├──► Thought: I should first check the table schema for customers and orders.
  ├──► Action: describe_schema('customers')
  ├──► Observation: Columns: id, name, email, tier...
  │
  ├──► Thought: Now I will aggregate orders grouped by customer ID.
  ├──► Action: run_sql("SELECT name, SUM(total_amount)...")
  ├──► Observation: [{"name": "Stark Industries", "total": 25000}]
  │
  └──► Final Answer: Stark Industries is the top customer with $25,000.
```

## Quickstart Usage
```python
from experiments.04_sql_react_agent.agent import SQLReActAgent

agent = SQLReActAgent()
result = agent.run("Show me the total revenue per sales region.")

for step in result["steps"]:
    print(f"[{step['action']}] -> {step['thought']}")
print("Final Answer:", result["final_answer"])
```
