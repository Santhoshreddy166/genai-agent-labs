"""
Unit tests for Module 09: Reasoning Model Benchmarking
"""

import pytest
from experiments import ReasoningBenchmarkHarness, get_reasoning_tasks


def test_reasoning_tasks_presence():
    tasks = get_reasoning_tasks()
    assert len(tasks) >= 3
    for t in tasks:
        assert "prompt" in t
        assert "validator_regex" in t


def test_benchmark_harness_run():
    harness = ReasoningBenchmarkHarness()
    res = harness.run_benchmark()
    assert "summary_df" in res
    assert "detailed_results" in res
    assert len(res["summary_df"]) == 4  # 4 strategies
