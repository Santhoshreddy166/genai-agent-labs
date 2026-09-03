# Module 07: Deep Research Agent Workflow

## Overview
This module implements an iterative research workflow based on the **Plan + Execute + Reflect + Refine** paradigm. Instead of generating a superficial single-turn summary, the agent autonomously formulates investigative research sub-goals, gathers evidence via multi-query search, reflects on information gaps, refines subsequent queries, and compiles an evidence-backed report with sources.

## Research Cycle
```
Research Topic Inquiry
          │
          ▼
      [Planning] ──────────► Formulate sub-hypotheses & target queries
          │
          ▼
     [Execution] ─────────► Web search / evidence gathering
          │
          ▼
     [Reflection] ────────► Analyze gaps, contradictions, or missing proof
          │
          ▼
     [Refinement] ────────► Branch follow-up queries
          │
          ▼
[Dossier Synthesis] ──────► Generate comprehensive cited research document
```

## Quickstart Usage
```python
from experiments.07_deep_research_agent.workflow import DeepResearchAgent

agent = DeepResearchAgent(max_iterations=2)
result = agent.run("Post-training quantization techniques for edge LLM inference")

print("Report Preview:\n", result["final_report"][:600])
```
