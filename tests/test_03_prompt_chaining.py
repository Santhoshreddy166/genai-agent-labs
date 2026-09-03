"""
Unit tests for Module 03: Prompt Chaining for Summarization
"""

import pytest
from experiments import PromptChainingSummarizer


def test_prompt_chaining_stages():
    summarizer = PromptChainingSummarizer()
    sample_text = (
        "Enterprise agents combine LLM reasoning with tools. "
        "Security guardrails prevent destructive database queries. "
        "Model quantization reduces memory usage by 78%."
    )
    res = summarizer.run(sample_text)

    assert "stage_1_key_points" in res
    assert "stage_2_chapter_summaries" in res
    assert "stage_3_executive_summary" in res
    assert len(res["telemetry"]) == 3
    assert res["total_duration_sec"] >= 0
