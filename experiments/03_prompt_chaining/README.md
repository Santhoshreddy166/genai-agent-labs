# Module 03: Multi-Stage Prompt Chaining Pipeline

## Overview
This module demonstrates the prompt chaining pattern to overcome context dilution and cognitive overload when summarizing complex documents. By decomposing the summarization task into three atomic, sequentially conditioned transformations, the system produces significantly higher-fidelity outputs than a single-shot prompt.

## Chain Flow
```
Long Raw Document
       │
       ▼
[Stage 1: Key Point Extraction] ──► Extracts factual statements & core metrics
       │
       ▼
[Stage 2: Thematic Clustering]   ──► Groups findings into structured chapters
       │
       ▼
[Stage 3: Executive Synthesis]   ──► Formulates C-suite briefing & recommendations
```

## Quickstart Usage
```python
from experiments.03_prompt_chaining.chains import PromptChainingSummarizer

summarizer = PromptChainingSummarizer()
doc = open("data/documents/enterprise_security_policy.txt", encoding="utf-8").read()
result = summarizer.run(doc)

print("Executive Summary:\n", result["stage_3_executive_summary"])
```
