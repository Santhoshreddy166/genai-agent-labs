"""
Hybrid Policy Compliance Evaluator combining regex checks with LLM judgment.
"""

from typing import Dict, Any, List
from src.utils import get_llm
from src.config import use_mock
from .rules import run_deterministic_rules


LLM_JUDGE_PROMPT = """You are a Principal AI Safety and Regulatory Compliance Auditor.
Analyze the provided text against enterprise compliance standards (PII exposure, financial guarantees, medical liability, and hate speech).

Text to audit:
"{text}"

Provide your evaluation in JSON format:
{{
    "status": "PASS" | "FLAGGED",
    "risk_score": 0-100,
    "violations": ["list of specific violations found"],
    "recommendations": "Actionable fixes for remediation"
}}
"""


class PolicyComplianceAgent:
    """Evaluates text payloads against deterministic policies and LLM semantic standards."""

    def __init__(self):
        self.llm = get_llm()

    def evaluate(self, text: str) -> Dict[str, Any]:
        """
        Runs two-tier audit:
        1. Fast deterministic regex scan
        2. Semantic LLM judge for context analysis
        """
        # Tier 1: Deterministic scan
        rule_violations = run_deterministic_rules(text)

        # Calculate base score
        base_penalty = 0
        for v in rule_violations:
            if v["severity"] == "CRITICAL":
                base_penalty += 45
            elif v["severity"] == "HIGH":
                base_penalty += 25
            else:
                base_penalty += 10

        risk_score = min(100, base_penalty)
        status = "FLAGGED" if risk_score >= 25 else "PASS"

        # Tier 2: LLM judge synthesis
        if use_mock():
            llm_notes = (
                "Deterministic inspection completed. "
                f"Identified {len(rule_violations)} policy breaches." if rule_violations
                else "Clean text payload. No high-risk regulatory or safety patterns detected."
            )
        else:
            prompt = LLM_JUDGE_PROMPT.format(text=text)
            resp = self.llm.invoke(prompt)
            llm_notes = getattr(resp, "content", str(resp))

        return {
            "text_preview": text[:140] + ("..." if len(text) > 140 else ""),
            "status": status,
            "risk_score": risk_score,
            "deterministic_violations": rule_violations,
            "llm_audit_summary": llm_notes,
            "is_compliant": status == "PASS"
        }
