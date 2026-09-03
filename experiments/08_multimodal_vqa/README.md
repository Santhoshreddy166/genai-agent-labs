# Module 08: Multimodal Visual QA System

## Overview
This module demonstrates visual question answering (VQA) using Vision-Language Models (e.g., GPT-4o). It accepts architectural diagrams, engineering schematics, or interface wireframes, extracts semantic features, retrieves supplementary enterprise textual documentation via vector similarity, and generates grounded contextual answers.

## Architecture
```
Input Image (Diagram/Schematic) + Natural Language Question
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
[Base64 Encoding & Preprocessing]  [Vector Context Retrieval]
         │                           │
         └─────────────┬─────────────┘
                       ▼
        [Multimodal Vision Prompt]
                       │
                       ▼
     [Vision-Language Model (GPT-4o)]
                       │
                       ▼
Structured Architectural Breakdown & Answers
```

## Quickstart Usage
```python
from experiments.08_multimodal_vqa.pipeline import MultimodalVQAPipeline
from experiments.08_multimodal_vqa.image_utils import generate_sample_diagram

pipeline = MultimodalVQAPipeline()
sample_img = generate_sample_diagram()

result = pipeline.analyze_image(
    image=sample_img,
    question="What components sit between the client app and the foundation model?"
)

print(result["answer"])
```
