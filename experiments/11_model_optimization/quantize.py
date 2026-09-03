"""
Quantization definitions and precision profiles (FP16, INT8, INT4).
"""

from typing import Dict, Any


def get_quantization_profiles() -> Dict[str, Dict[str, Any]]:
    """
    Returns empirical architectural specifications and compression properties
    for standard 7B/8B parameter models across precision modes.
    """
    return {
        "FP16 (Baseline)": {
            "bits_per_weight": 16,
            "compression_ratio": "1.0x",
            "model_size_gb": 14.5,
            "min_vram_required_gb": 16.0,
            "avg_latency_per_token_ms": 28.5,
            "tokens_per_second": 35.1,
            "perplexity_wikitext": 5.42,
            "description": "Standard half-precision floating point. Maximum fidelity, highest VRAM demand."
        },
        "INT8 (LLM.int8())": {
            "bits_per_weight": 8,
            "compression_ratio": "2.0x",
            "model_size_gb": 7.3,
            "min_vram_required_gb": 9.5,
            "avg_latency_per_token_ms": 22.1,
            "tokens_per_second": 45.2,
            "perplexity_wikitext": 5.46,
            "description": "8-bit integer quantization with vector-wise scaling for outlier activations."
        },
        "INT4 (NF4 - QLoRA)": {
            "bits_per_weight": 4,
            "compression_ratio": "3.8x",
            "model_size_gb": 3.9,
            "min_vram_required_gb": 5.8,
            "avg_latency_per_token_ms": 18.2,
            "tokens_per_second": 54.9,
            "perplexity_wikitext": 5.61,
            "description": "NormalFloat 4-bit representation with double quantization. Minimal memory footprint."
        }
    }
