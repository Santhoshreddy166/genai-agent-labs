"""
Reasoning prompting strategies: Zero-Shot, Few-Shot, CoT, and Tree-of-Thought (ToT).
"""

from typing import Dict, Any
from src.utils import get_llm
from src.config import use_mock


class BaseStrategy:
    def __init__(self):
        self.llm = get_llm()

    def run(self, prompt: str) -> str:
        raise NotImplementedError


class ZeroShotStrategy(BaseStrategy):
    """Zero-shot direct question prompt."""
    def run(self, prompt: str) -> str:
        if use_mock():
            return "Based on direct computation, the answer is 45.33%."
        formatted = f"Answer the following question directly and concisely:\n{prompt}\nAnswer:"
        resp = self.llm.invoke(formatted)
        return getattr(resp, "content", str(resp))


class FewShotStrategy(BaseStrategy):
    """Few-shot prompt with in-context exemplary demonstrations."""
    EXEMPLARS = """Example 1:
Question: A jar has 10 blue and 20 red marbles. If we add 5 blue marbles, what % of the jar is blue?
Answer: Initially 10 blue out of 30 total. After adding 5 blue, there are 15 blue out of 35 total. 15 / 35 = 42.86%.

Example 2:
Question: Task X takes 2 hours. Task Y depends on Task X and takes 3 hours. Minimum total time?
Answer: Task X runs from t=0 to t=2. Task Y runs from t=2 to t=5. Total is 5 hours.
"""

    def run(self, prompt: str) -> str:
        if use_mock():
            return "Following the examples: Total engineers = 48 + 20 = 68. Total people = 150. 68/150 = 45.33%."
        formatted = f"{self.EXEMPLARS}\nNow solve this question:\nQuestion: {prompt}\nAnswer:"
        resp = self.llm.invoke(formatted)
        return getattr(resp, "content", str(resp))


class ChainOfThoughtStrategy(BaseStrategy):
    """Step-by-step reasoning elicitation."""
    def run(self, prompt: str) -> str:
        if use_mock():
            return (
                "Let's think step by step:\n"
                "1. Initial workforce = 120 employees. 40% are engineers: 120 * 0.40 = 48 engineers.\n"
                "2. 20 new engineers are hired: 48 + 20 = 68 engineers.\n"
                "3. 10 non-engineers are hired: 120 + 20 + 10 = 150 total employees.\n"
                "4. Fraction of engineers = 68 / 150 = 0.45333... = 45.33%.\n"
                "Final Answer: 45.33%"
            )
        formatted = f"Solve the problem step-by-step. Detail every calculation before stating the final answer.\nQuestion: {prompt}\nDetailed Reasoning:"
        resp = self.llm.invoke(formatted)
        return getattr(resp, "content", str(resp))


class TreeOfThoughtStrategy(BaseStrategy):
    """
    Tree-of-Thought (ToT) exploration:
    Generates multiple branching candidate hypotheses, evaluates each,
    and synthesizes the most coherent path.
    """
    def run(self, prompt: str) -> str:
        if use_mock():
            return (
                "--- Tree-of-Thought Exploration ---\n"
                "Branch A (Direct Ratio): Assume non-engineers don't affect total count -> Flawed.\n"
                "Branch B (Incremental Counting): Track initial engineers (48), new additions (20), new total (150) -> Valid & robust.\n"
                "Branch C (Algebraic Variable): Set E_f = 68, T_f = 150, ratio = 68/150 = 45.33% -> Valid.\n"
                "Synthesis & Pruning: Branch B & C converge on 45.33%.\n"
                "Final Verified Answer: 45.33%"
            )
        formatted = (
            f"You are applying the Tree-of-Thought (ToT) problem-solving framework.\n"
            f"Problem: {prompt}\n\n"
            f"1. Generate 3 distinct reasoning branches or perspectives (Branch 1, Branch 2, Branch 3).\n"
            f"2. Evaluate each branch for factual and logical consistency, pruning errors.\n"
            f"3. Converge on the optimal verified solution.\n\n"
            f"Tree of Thought Analysis:"
        )
        resp = self.llm.invoke(formatted)
        return getattr(resp, "content", str(resp))
