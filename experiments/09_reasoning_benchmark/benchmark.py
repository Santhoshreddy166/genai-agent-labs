"""
Benchmark execution harness comparing reasoning strategies.
"""

import re
import time
import pandas as pd
from typing import List, Dict, Any
from .tasks import get_reasoning_tasks
from .strategies import (
    ZeroShotStrategy,
    FewShotStrategy,
    ChainOfThoughtStrategy,
    TreeOfThoughtStrategy
)


class ReasoningBenchmarkHarness:
    """Runs reasoning benchmarks across multiple strategies and computes comparative metrics."""

    def __init__(self):
        self.strategies = {
            "Zero-Shot": ZeroShotStrategy(),
            "Few-Shot": FewShotStrategy(),
            "Chain-of-Thought (CoT)": ChainOfThoughtStrategy(),
            "Tree-of-Thought (ToT)": TreeOfThoughtStrategy()
        }

    def run_benchmark(self) -> Dict[str, Any]:
        tasks = get_reasoning_tasks()
        results: List[Dict[str, Any]] = []

        for task in tasks:
            for strat_name, strat_impl in self.strategies.items():
                t0 = time.time()
                output = strat_impl.run(task["prompt"])
                latency = round(time.time() - t0, 3)

                # Check validation regex
                is_correct = bool(re.search(task["validator_regex"], output, re.IGNORECASE))

                results.append({
                    "task_id": task["id"],
                    "category": task["category"],
                    "strategy": strat_name,
                    "latency_sec": latency,
                    "correct": is_correct,
                    "output_length": len(output),
                    "output_preview": output[:180].replace("\n", " ") + "..."
                })

        df = pd.DataFrame(results)
        
        # Aggregate stats
        summary = df.groupby("strategy").agg(
            accuracy=("correct", "mean"),
            avg_latency_sec=("latency_sec", "mean"),
            avg_output_chars=("output_length", "mean")
        ).reset_index()

        summary["accuracy_pct"] = (summary["accuracy"] * 100).round(1)
        summary["avg_latency_sec"] = summary["avg_latency_sec"].round(3)
        summary["avg_output_chars"] = summary["avg_output_chars"].round(1)

        return {
            "detailed_results": results,
            "summary_df": summary,
            "raw_df": df
        }
