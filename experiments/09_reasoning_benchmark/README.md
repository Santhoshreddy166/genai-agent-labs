# Module 09: Reasoning Model Benchmarking Suite

## Overview
This module benchmarks prompting architectures across complex multi-step reasoning, deductive logic, and algorithmic constraint tasks. It systematically measures and profiles:
- **Zero-Shot Prompting**: Baseline direct querying.
- **Few-Shot Prompting**: Providing structured exemplars in the context window.
- **Chain-of-Thought (CoT)**: Enforcing step-by-step intermediate calculation traces.
- **Tree-of-Thought (ToT)**: Generating branching reasoning trees with evaluation, pruning, and convergence.

## Metrics Tracked
1. **Task Accuracy (%)**: Ground-truth pattern validation.
2. **Inference Latency (sec)**: End-to-end execution duration.
3. **Cognitive Overhead (characters/tokens)**: Intermediate thought expansion.

## Quickstart Usage
```python
from experiments.09_reasoning_benchmark.benchmark import ReasoningBenchmarkHarness

harness = ReasoningBenchmarkHarness()
results = harness.run_benchmark()

print("Summary Benchmark Table:")
print(results["summary_df"].to_string(index=False))
```
