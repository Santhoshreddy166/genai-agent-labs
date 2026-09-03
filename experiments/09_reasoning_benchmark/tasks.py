"""
Reasoning benchmark tasks and ground-truth validation suite.
"""

from typing import List, Dict, Any

REASONING_TASKS: List[Dict[str, Any]] = [
    {
        "id": "TASK-MATH-01",
        "category": "Multi-Step Arithmetic & Logic",
        "prompt": "A company has 120 employees. 40% are engineers. If the company hires 20 more engineers and 10 non-engineers, what percentage of the new total workforce are engineers? Provide the final numerical percentage.",
        "expected_answer": "45.33%",
        "validator_regex": r'45(?:\.33)?%?'
    },
    {
        "id": "TASK-LOGIC-02",
        "category": "Deductive Reasoning",
        "prompt": "Alice, Bob, and Charlie sit in a row. Alice never sits next to Bob. Charlie is sitting to the right of Alice. Who is in the middle? Answer with the person's name only.",
        "expected_answer": "Charlie",
        "validator_regex": r'\bCharlie\b'
    },
    {
        "id": "TASK-SYS-03",
        "category": "Algorithmic Constraints",
        "prompt": "You have 3 tasks: A (takes 4 hours), B (takes 2 hours), C (takes 3 hours). Task B depends on Task A. Task C can run in parallel with Task A. What is the minimum total duration in hours to complete all tasks?",
        "expected_answer": "6 hours",
        "validator_regex": r'\b6\b'
    }
]


def get_reasoning_tasks() -> List[Dict[str, Any]]:
    return REASONING_TASKS
