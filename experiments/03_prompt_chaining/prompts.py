"""
Prompt templates for sequential multi-stage summarization chaining.
"""

STAGE_1_EXTRACT_KEY_POINTS = """You are an expert Research Analyst.
Read the source text below and extract all primary factual claims, metrics, architectural points, and key assertions.
Format your output as a numbered list of concise bullet points.

Source Text:
{source_text}

Extracted Key Points:
"""

STAGE_2_CHAPTER_SYNTHESIS = """You are a Lead Technical Editor.
Given the following raw extracted key points, group them into thematic chapters or categories (e.g., Architecture, Governance, Performance, Business Impact).
Write a cohesive synthesis for each section.

Extracted Key Points:
{key_points}

Thematic Chapter Summaries:
"""

STAGE_3_EXECUTIVE_SUMMARY = """You are a Chief Technology Officer (CTO).
Based on the thematic chapter summaries below, write a high-impact Executive Summary suitable for board members and senior engineering leadership.

Include:
1. Executive Overview (2-3 sentences)
2. Strategic Implications
3. Core Technical Decisions & Guardrails
4. Recommended Next Steps

Chapter Summaries:
{chapter_summaries}

Executive Summary:
"""
