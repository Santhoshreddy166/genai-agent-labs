# Module 06: Enterprise Policy Compliance Agent

## Overview
This module implements a hybrid compliance and safety verification system designed to intercept regulatory, legal, and operational risks in LLM inputs and outputs. It blends fast, sub-millisecond regex scanners with deep LLM judging to identify PII leaks, unauthorized financial promises, and unverified medical advice.

## Two-Tier Audit Architecture
```
Incoming Text (Prompt or Model Generation)
                   │
                   ▼
     [Tier 1: Deterministic Scanner]
  ├── PII (Email, Credit Card Numbers)
  ├── Financial Guarantees (100% risk-free)
  └── Medical Liability
                   │
                   ▼
     [Tier 2: Semantic LLM Judge]
  ├── Subtext, sarcasm, evasive phrasing
  └── Contextual risk scoring (0-100)
                   │
                   ▼
Compliance Report & Remediation Recommendations
```

## Quickstart Usage
```python
from experiments.06_policy_compliance.evaluator import PolicyComplianceAgent

agent = PolicyComplianceAgent()
sample_text = "Here is Tony's private email tony@stark.org and card 4111222233334444."
result = agent.evaluate(sample_text)

print("Compliance Status:", result["status"])
print("Risk Score:", result["risk_score"])
print("Violations:", [v["name"] for v in result["deterministic_violations"]])
```
