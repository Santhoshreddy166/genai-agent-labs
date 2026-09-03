"""
Compliance rules, regex patterns, and policy definitions.
"""

import re
from typing import Dict, Any, List

RULES = [
    {
        "id": "RULE-PII-001",
        "name": "Customer Email Exposure",
        "category": "Data Privacy (GDPR/CCPA)",
        "severity": "CRITICAL",
        "description": "Cleartext personal email addresses must not be exposed in model outputs.",
        "regex": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
        "remediation": "Replace email address with masked token [EMAIL_REDACTED]."
    },
    {
        "id": "RULE-PII-002",
        "name": "Credit Card / Payment Token Exposure",
        "category": "PCI-DSS",
        "severity": "CRITICAL",
        "description": "Payment card numbers (13-16 digits) must not be transmitted.",
        "regex": r'\b(?:\d[ -]*?){13,16}\b',
        "remediation": "Mask card numbers showing only last 4 digits (e.g., ****-****-****-1234)."
    },
    {
        "id": "RULE-FIN-003",
        "name": "Guaranteed Investment Returns",
        "category": "Financial Regulatory Compliance (SEC/FINRA)",
        "severity": "HIGH",
        "description": "Statements guaranteeing specific ROI, profits, or infallible returns are prohibited.",
        "regex": r'(?:guarantee[ds]?\s+(?:profit|return|yield|roi)|100%\s+risk-free|assured\s+returns)',
        "remediation": "Add regulatory disclaimer: 'Past performance does not guarantee future results.'"
    },
    {
        "id": "RULE-MED-004",
        "name": "Unverified Medical Diagnoses",
        "category": "Healthcare Disclaimers",
        "severity": "HIGH",
        "description": "Agent must not provide definitive clinical medical diagnoses.",
        "regex": r'(?:you\s+(?:definitely|certainly)\s+have\s+(?:cancer|diabetes|covid|hypertension))',
        "remediation": "Recommend consulting a licensed healthcare professional."
    }
]


def run_deterministic_rules(text: str) -> List[Dict[str, Any]]:
    """Evaluates text against deterministic regex patterns."""
    violations = []
    for rule in RULES:
        matches = list(re.finditer(rule["regex"], text, re.IGNORECASE))
        if matches:
            matched_snippets = [m.group(0) for m in matches[:3]]
            violations.append({
                "rule_id": rule["id"],
                "name": rule["name"],
                "category": rule["category"],
                "severity": rule["severity"],
                "matches": matched_snippets,
                "remediation": rule["remediation"]
            })
    return violations
