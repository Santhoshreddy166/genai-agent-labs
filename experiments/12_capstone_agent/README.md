# Module 12: Mini Project (Capstone) — Agentic Multi-Tool RAG System

## Overview
The Capstone Module synthesizes the learnings from the preceding 11 experiments into an enterprise-grade, multi-tool autonomous agent. It features intent routing, safe relational Text-to-SQL querying, semantic RAG over internal knowledge documents, and automated Policy Compliance evaluation on synthesized outputs.

## Capstone System Architecture
```
                   User Query Ingestion
                            │
                            ▼
              [Supervisor Intent Classifier]
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
       [Relational SQL]  [Hybrid]   [Semantic RAG]
        (Customers, DB)             (Policies, Docs)
              │             │             │
              └─────────────┬─────────────┘
                            ▼
               [Answer Synthesis Engine]
                            │
                            ▼
           [Real-Time Policy Compliance Audit]
             ├── Pass (Score: 0)  ──► Final Answer
             └── Flagged (Score > 0) ──► Alert & Sanitize
```

## Quickstart Usage
```python
from experiments.12_capstone_agent.agent import CapstoneAgent

agent = CapstoneAgent()

# 1. Relational SQL query
res_sql = agent.run("Show me all Enterprise tier customers.")
print(res_sql["final_answer"])

# 2. Policy & Architecture query
res_rag = agent.run("What are the security guidelines for handling PII?")
print(res_rag["final_answer"])
```
