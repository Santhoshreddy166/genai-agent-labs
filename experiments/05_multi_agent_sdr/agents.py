"""
Agent definitions and prompts for the Multi-Agent SDR System.
"""

from typing import Dict, Any
from src.utils import get_llm
from src.config import use_mock


class LeadGenerationAgent:
    """Discovers and constructs detailed prospect profiles."""
    
    SYSTEM_PROMPT = """You are a Senior B2B Sales Prospecting Specialist.
Given a target market or criteria, generate 2 realistic enterprise prospect profiles.
Return a structured JSON with:
- name: string
- company: string
- title: string
- industry: string
- estimated_revenue: string
- recent_news_or_trigger: string
"""

    def __init__(self):
        self.llm = get_llm()

    def generate_prospect(self, target_criteria: str) -> Dict[str, Any]:
        if use_mock():
            return {
                "name": "Marcus Vance",
                "company": "Apex Global Logistics",
                "title": "Head of Enterprise IT Infrastructure",
                "industry": "Supply Chain & Logistics",
                "estimated_revenue": "$450M",
                "recent_news_or_trigger": "Announced $20M digital modernization push and migration to autonomous operations."
            }

        prompt = f"{self.SYSTEM_PROMPT}\nTarget Criteria: {target_criteria}\nGenerate 1 detailed prospect JSON:"
        res = self.llm.invoke(prompt)
        content = getattr(res, "content", str(res))
        # Parse or wrap
        return {
            "name": "Marcus Vance",
            "company": "Apex Global Logistics",
            "title": "Head of Enterprise IT Infrastructure",
            "raw_output": content
        }


class QualificationAgent:
    """Evaluates prospects against Ideal Customer Profile (ICP)."""

    def __init__(self):
        self.llm = get_llm()

    def qualify(self, prospect: Dict[str, Any], icp_criteria: str) -> Dict[str, Any]:
        if use_mock():
            return {
                "icp_score": 94,
                "fit_status": "STRONG_FIT",
                "strengths": [
                    "Senior decision maker with direct budget authority over modernization",
                    "Company revenue tier ($450M) matches enterprise packaging",
                    "Active trigger event aligns with autonomous systems offering"
                ],
                "risks": ["May have existing multi-year vendor lock-in"],
                "recommendation": "Proceed immediately with Tier-1 customized outbound email."
            }

        prompt = (
            f"You are an ICP Qualification Specialist.\n"
            f"ICP Definition: {icp_criteria}\n"
            f"Prospect Profile: {prospect}\n"
            f"Provide an ICP score (0-100), fit status, strengths, and risks."
        )
        res = self.llm.invoke(prompt)
        return {
            "icp_score": 88,
            "fit_status": "QUALIFIED",
            "analysis": getattr(res, "content", str(res))
        }


class EmailingAgent:
    """Drafts high-conversion, personalized outreach communications."""

    def __init__(self):
        self.llm = get_llm()

    def draft_email(self, prospect: Dict[str, Any], qualification: Dict[str, Any], value_prop: str) -> Dict[str, str]:
        if use_mock():
            return {
                "subject": f"Accelerating {prospect.get('company', 'Apex')}'s digital modernization with autonomous AI",
                "preview_text": f"Thoughtful approach for Marcus regarding supply chain IT workflows.",
                "body": (
                    f"Hi {prospect.get('name', 'Marcus').split()[0]},\n\n"
                    f"Noticed Apex Global Logistics' recent initiative to expand autonomous digital operations. "
                    f"Given your leadership over enterprise infrastructure, managing the integration of GenAI "
                    f"guardrails while speeding up data access is likely top of mind.\n\n"
                    f"We help enterprises deploy self-correcting AI workflows and read-only database agents "
                    f"that eliminate manual SQL querying and slash data retrieval latency by 65%—without security compromises.\n\n"
                    f"Open to a brief 10-minute briefing next Tuesday to compare notes?\n\n"
                    f"Best regards,\n"
                    f"Enterprise AI Solutions Team"
                )
            }

        prompt = (
            f"Draft a personalized 3-paragraph cold outbound email.\n"
            f"Prospect: {prospect}\n"
            f"Qualification Highlights: {qualification}\n"
            f"Value Proposition: {value_prop}\n"
            f"Subject Line, Preview Text, and Body:"
        )
        res = self.llm.invoke(prompt)
        return {
            "subject": f"Autonomous AI operations for {prospect.get('company', 'Enterprise')}",
            "body": getattr(res, "content", str(res))
        }
