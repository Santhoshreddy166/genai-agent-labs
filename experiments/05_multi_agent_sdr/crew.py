"""
Multi-Agent SDR workflow orchestration.
Coordinates Lead Generation -> Qualification -> Email Outreach.
"""

from typing import Dict, Any
from .agents import (
    LeadGenerationAgent,
    QualificationAgent,
    EmailingAgent
)


class SDRMultiAgentWorkflow:
    """Orchestrates the end-to-end multi-agent sales development workflow."""

    def __init__(self):
        self.lead_gen_agent = LeadGenerationAgent()
        self.qualification_agent = QualificationAgent()
        self.emailing_agent = EmailingAgent()

    def run_campaign(
        self,
        target_industry: str = "Enterprise Logistics & Supply Chain",
        icp_criteria: str = "B2B Companies with >$100M revenue looking to deploy AI workflows",
        value_proposition: str = "Autonomous data agents with built-in AST safety guardrails"
    ) -> Dict[str, Any]:
        """
        Executes sequential pipeline:
        1. LeadGen discovers/synthesizes prospect
        2. Qualification evaluates ICP alignment
        3. Emailer composes tailored outreach email
        """
        # Step 1: Discover Prospect
        prospect = self.lead_gen_agent.generate_prospect(target_industry)

        # Step 2: Qualify Prospect
        qualification = self.qualification_agent.qualify(prospect, icp_criteria)

        # Step 3: Draft Outreach
        email_draft = self.emailing_agent.draft_email(
            prospect=prospect,
            qualification=qualification,
            value_prop=value_proposition
        )

        return {
            "campaign_target": target_industry,
            "prospect": prospect,
            "qualification": qualification,
            "outreach_email": email_draft,
            "status": "READY_FOR_HUMAN_REVIEW"
        }
