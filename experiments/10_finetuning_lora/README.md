# Module 10: Fine-Tuning for Domain Adaptation (PEFT / QLoRA)

## Overview
This module demonstrates Parameter-Efficient Fine-Tuning (PEFT) using **QLoRA (Quantized Low-Rank Adaptation)**. By freezing 4-bit quantized base foundation model weights (NF4) and injecting low-rank adapter matrices (r=16, alpha=32) into key attention projections (`q_proj`, `v_proj`, etc.), QLoRA slashes GPU VRAM consumption by ~78% while preserving over 99% of full fine-tuning performance.

## Mathematical Formulation
$$\Delta W = B \cdot A$$
Where:
- $W \in \mathbb{R}^{d \times k}$ is the frozen 4-bit pre-trained weight matrix.
- $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ are low-rank adapter matrices with rank $r \ll \min(d, k)$.
- Trainable parameter footprint drops from 7,000,000,000 to ~16,770,000 (a **99.76% reduction**).

## Quickstart Usage
```python
from experiments.10_finetuning_lora.train import run_qlora_training

# Run training (uses dry-run simulation mode on standard CPUs/CI)
results = run_qlora_training(dry_run=True)
print("Parameter Reduction Ratio:", results["parameter_efficiency"]["parameter_reduction_ratio"])
print("VRAM Savings:", results["vram_savings_pct"])
```
