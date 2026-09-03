"""
Multi-stage Prompt Chaining pipeline for deep document summarization.
"""

import time
from typing import Dict, Any
from src.utils import get_llm
from src.config import use_mock
from .prompts import (
    STAGE_1_EXTRACT_KEY_POINTS,
    STAGE_2_CHAPTER_SYNTHESIS,
    STAGE_3_EXECUTIVE_SUMMARY
)


class PromptChainingSummarizer:
    """Executes a 3-stage prompt chain pipeline."""

    def __init__(self):
        self.llm = get_llm()

    def run(self, source_text: str) -> Dict[str, Any]:
        """
        Executes:
        Stage 1: Key Points Extraction
        Stage 2: Thematic Chapter Synthesis
        Stage 3: Executive CTO Briefing
        """
        start_time = time.time()
        telemetry = []

        # --- Stage 1: Key Points ---
        t0 = time.time()
        if use_mock():
            stage_1_output = (
                "1. Autonomous agents require ReAct reasoning loops (Thought -> Action -> Observation).\n"
                "2. Security guardrails must prevent destructive SQL operations (DROP/DELETE/ALTER).\n"
                "3. RAG systems must implement cosine similarity distance cutoffs to halt hallucinations.\n"
                "4. Quantization (INT4/NF4) enables low-footprint deployment on edge hardware."
            )
        else:
            p1 = STAGE_1_EXTRACT_KEY_POINTS.format(source_text=source_text)
            r1 = self.llm.invoke(p1)
            stage_1_output = getattr(r1, "content", str(r1))

        telemetry.append({
            "stage": "Stage 1: Key Points Extraction",
            "duration_sec": round(time.time() - t0, 2),
            "output_chars": len(stage_1_output)
        })

        # --- Stage 2: Chapter Synthesis ---
        t1 = time.time()
        if use_mock():
            stage_2_output = (
                "### Chapter 1: Agentic Orchestration\n"
                "The core engine relies on interleaved verbal reasoning and atomic tool invocation.\n\n"
                "### Chapter 2: Security & Governance\n"
                "Strict database AST inspection and PII tokenization protect enterprise data assets.\n\n"
                "### Chapter 3: Model Efficiency\n"
                "Quantization and QLoRA reduce infrastructure overhead while maintaining accuracy."
            )
        else:
            p2 = STAGE_2_CHAPTER_SYNTHESIS.format(key_points=stage_1_output)
            r2 = self.llm.invoke(p2)
            stage_2_output = getattr(r2, "content", str(r2))

        telemetry.append({
            "stage": "Stage 2: Thematic Chapter Synthesis",
            "duration_sec": round(time.time() - t1, 2),
            "output_chars": len(stage_2_output)
        })

        # --- Stage 3: Executive Summary ---
        t2 = time.time()
        if use_mock():
            stage_3_output = (
                "## Executive Briefing: AI Systems Transformation\n\n"
                "### 1. Executive Overview\n"
                "Adoption of agentic architectures combined with local vector grounding delivers high operational velocity while mitigating compliance exposure.\n\n"
                "### 2. Strategic Implications\n"
                "- Automation of data queries through self-correcting SQL pipelines.\n"
                "- Lower cloud compute expenditure via INT4/INT8 model quantization.\n\n"
                "### 3. Core Recommendations\n"
                "- Enforce read-only database connections for all autonomous agents.\n"
                "- Mandate ground-truth citation logging across all customer-facing pipelines."
            )
        else:
            p3 = STAGE_3_EXECUTIVE_SUMMARY.format(chapter_summaries=stage_2_output)
            r3 = self.llm.invoke(p3)
            stage_3_output = getattr(r3, "content", str(r3))

        telemetry.append({
            "stage": "Stage 3: Executive CTO Summary",
            "duration_sec": round(time.time() - t2, 2),
            "output_chars": len(stage_3_output)
        })

        total_duration = round(time.time() - start_time, 2)

        return {
            "source_char_count": len(source_text),
            "total_duration_sec": total_duration,
            "telemetry": telemetry,
            "stage_1_key_points": stage_1_output,
            "stage_2_chapter_summaries": stage_2_output,
            "stage_3_executive_summary": stage_3_output
        }
