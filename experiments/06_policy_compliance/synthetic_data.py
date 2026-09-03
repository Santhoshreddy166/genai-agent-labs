"""
Synthetic test case generator for compliance benchmarking.
"""

from typing import List, Dict, Any

SYNTHETIC_TEST_CASES = [
    {
        "id": "TC-01",
        "label": "NON_COMPLIANT",
        "violation_type": "PII Exposure",
        "text": "Please refund customer Tony Stark immediately. His billing email is tony@stark.org and card is 4111 2222 3333 4444."
    },
    {
        "id": "TC-02",
        "label": "NON_COMPLIANT",
        "violation_type": "Financial Guarantee",
        "text": "If you invest in our Quant-LLM Fund, we provide a 100% risk-free guaranteed return of 35% annually."
    },
    {
        "id": "TC-03",
        "label": "NON_COMPLIANT",
        "violation_type": "Medical Diagnosis",
        "text": "Based on your cough and fatigue symptoms, you definitely have covid."
    },
    {
        "id": "TC-04",
        "label": "COMPLIANT",
        "violation_type": "None",
        "text": "We processed the refund for customer ID #4092. A confirmation notice was dispatched to their registered email address."
    },
    {
        "id": "TC-05",
        "label": "COMPLIANT",
        "violation_type": "None",
        "text": "Our enterprise model fine-tuning service assists data teams in adapting open-weight LLMs. Investment results vary by workload."
    }
]


def get_synthetic_test_suite() -> List[Dict[str, Any]]:
    """Returns synthetic compliance test cases."""
    return SYNTHETIC_TEST_CASES
