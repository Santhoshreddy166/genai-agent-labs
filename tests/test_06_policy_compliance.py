"""
Unit tests for Module 06: Policy Compliance Agent
"""

import pytest
from experiments import (
    run_deterministic_rules,
    PolicyComplianceAgent,
    get_synthetic_test_suite
)


def test_deterministic_email_exposure():
    text = "Send customer data to test_user@enterprise.org immediately."
    violations = run_deterministic_rules(text)
    assert len(violations) >= 1
    assert violations[0]["rule_id"] == "RULE-PII-001"


def test_deterministic_credit_card_exposure():
    text = "Card number is 4111 2222 3333 4444."
    violations = run_deterministic_rules(text)
    assert any(v["rule_id"] == "RULE-PII-002" for v in violations)


def test_policy_agent_synthetic_suite():
    agent = PolicyComplianceAgent()
    test_cases = get_synthetic_test_suite()

    for tc in test_cases:
        res = agent.evaluate(tc["text"])
        if tc["label"] == "NON_COMPLIANT":
            assert res["is_compliant"] is False
            assert res["risk_score"] > 0
        else:
            assert res["is_compliant"] is True
            assert res["risk_score"] == 0
