# Module 11: Model Optimization Lab (Quantization & Latency Profiling)

## Overview
This module explores post-training quantization techniques to optimize large language model deployment. It systematically benchmarks **FP16 (Half Precision)**, **INT8 (LLM.int8())**, and **INT4 (NF4)** across critical hardware metrics:
- **VRAM Memory Footprint (GB)**
- **Per-Token Latency (ms)**
- **Generation Throughput (tokens/sec)**
- **Perplexity & Model Quality Degradation (WikiText-2)**

## Precision Modes Compared
| Precision Mode | Bits/Weight | Model Size (7B) | Min VRAM | Throughput | Perplexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FP16 (Baseline)** | 16-bit | 14.5 GB | 16.0 GB | 35.1 tok/s | 5.42 |
| **INT8 (LLM.int8)** | 8-bit | 7.3 GB | 9.5 GB | 45.2 tok/s | 5.46 |
| **INT4 (NF4)** | 4-bit | 3.9 GB | 5.8 GB | 54.9 tok/s | 5.61 |

## Quickstart Usage
```python
from experiments.11_model_optimization.benchmark import ModelOptimizationBenchmark

bench = ModelOptimizationBenchmark()
results = bench.run_benchmark_suite(tokens_to_generate=128)

print(results["results_table"].to_string(index=False))
```
