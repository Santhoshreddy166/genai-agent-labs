"""
Dataset preparation and instruction formatting for LoRA / QLoRA fine-tuning.
"""

from typing import List, Dict, Any

SAMPLE_ENTERPRISE_INSTRUCTIONS = [
    {
        "instruction": "Translate the customer request to read-only SQLite: 'Show me all Enterprise tier customers from USA.'",
        "input": "",
        "output": "SELECT * FROM customers WHERE tier = 'Enterprise' AND country = 'USA';"
    },
    {
        "instruction": "Format an AST guardrail security warning for a blocked query attempting to DROP TABLE orders.",
        "input": "",
        "output": "SECURITY ALERT: Destructive SQL keyword 'DROP' is forbidden. Operation halted."
    },
    {
        "instruction": "Evaluate the compliance risk of the following output: 'Card number 4111-2222-3333-4444 approved.'",
        "input": "",
        "output": "CRITICAL VIOLATION: Unmasked PCI payment card digits detected. Output must be tokenized."
    },
    {
        "instruction": "Explain the difference between INT8 vector quantization and 4-bit NormalFloat (NF4).",
        "input": "",
        "output": "INT8 quantization maps weights to 8-bit integers using uniform or vector-wise scaling. NF4 (NormalFloat4) builds an optimal information-theoretic quantile codebook specifically designed for normally distributed neural network weights, preserving accuracy at extreme 4-bit compression."
    }
]


def format_instruction(sample: Dict[str, str]) -> str:
    """Formats an instruction sample into standard LLM training template."""
    inst = sample["instruction"]
    inp = f"\nContext: {sample['input']}" if sample.get("input") else ""
    out = sample["output"]
    return f"<s>[INST] {inst}{inp} [/INST] {out} </s>"


def get_formatted_dataset() -> List[str]:
    """Returns a formatted list of training prompt strings."""
    return [format_instruction(sample) for sample in SAMPLE_ENTERPRISE_INSTRUCTIONS]
