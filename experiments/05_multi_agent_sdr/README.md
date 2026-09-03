# Module 05: Multi-Agent SDR (Sales Development Representative) System

## Overview
This module demonstrates specialized multi-agent collaboration for enterprise outbound sales workflows. Instead of relying on a monolithic prompt, three focused agents handle distinct responsibilities with strict input/output contract enforcement:

1. **Lead Generation Agent**: Generates target decision-maker profiles, company attributes, and recent news triggers.
2. **Qualification Agent**: Evaluates prospect alignment against an Ideal Customer Profile (ICP), scoring fit from 0 to 100 and analyzing operational risks.
3. **Emailing Agent**: Synthesizes the prospect's background, qualification findings, and value proposition into high-converting outbound emails.

## Multi-Agent Architecture
```
Target ICP & Industry Criteria
              │
              ▼
    [Lead Generation Agent]
              │
     Prospect Profile (JSON)
              │
              ▼
     [Qualification Agent]
              │
      ICP Score & Analysis
              │
              ▼
       [Emailing Agent]
              │
              ▼
Personalized Outbound Email (Ready for Human Review)
```

## Quickstart Usage
```python
from experiments.05_multi_agent_sdr.crew import SDRMultiAgentWorkflow

workflow = SDRMultiAgentWorkflow()
result = workflow.run_campaign(
    target_industry="Fintech & Digital Banking",
    icp_criteria="Companies >$200M revenue adopting LLMs for financial analytics",
    value_proposition="Audit-ready GenAI pipelines with compliance guardrails"
)

print("ICP Score:", result["qualification"]["icp_score"])
print("Subject:", result["outreach_email"]["subject"])
print("Body:\n", result["outreach_email"]["body"])
```
