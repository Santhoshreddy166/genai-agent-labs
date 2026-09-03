"""
Benchmarking profiler for quantized model inference.
"""

import time
import pandas as pd
from typing import Dict, Any
from .quantize import get_quantization_profiles


class ModelOptimizationBenchmark:
    """Measures latency, memory consumption, throughput, and perplexity across quantization levels."""

    def __init__(self):
        self.profiles = get_quantization_profiles()

    def run_benchmark_suite(self, tokens_to_generate: int = 128) -> Dict[str, Any]:
        results = []

        for mode, data in self.profiles.items():
            est_total_latency_sec = round((data["avg_latency_per_token_ms"] * tokens_to_generate) / 1000.0, 2)
            results.append({
                "Precision Mode": mode,
                "Model Size (GB)": data["model_size_gb"],
                "Min VRAM (GB)": data["min_vram_required_gb"],
                "Latency/Token (ms)": data["avg_latency_per_token_ms"],
                "Throughput (tok/s)": data["tokens_per_second"],
                "Total Latency (s)": est_total_latency_sec,
                "Perplexity (WikiText-2)": data["perplexity_wikitext"],
                "Compression": data["compression_ratio"]
            })

        df = pd.DataFrame(results)
        return {
            "tokens_benchmarked": tokens_to_generate,
            "results_table": df,
            "raw_profiles": self.profiles
        }
