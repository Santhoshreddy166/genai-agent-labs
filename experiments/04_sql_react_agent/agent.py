"""
ReAct (Reason + Act) SQL Agent with tool use and safety guardrails.
"""

import re
import json
from typing import Dict, Any, List
from src.utils import get_llm
from src.config import use_mock
from .tools import (
    tool_list_tables,
    tool_describe_schema,
    tool_run_sql
)
from .guardrails import check_sql_safety


REACT_SYSTEM_PROMPT = """You are an autonomous SQL ReAct Agent.
You solve user data inquiries step-by-step using tools.

You have access to the following tools:
1. `list_tables`: List all tables in the database. Argument: none (pass empty string).
2. `describe_schema`: Get column definitions. Argument: table_name (or empty string for all tables).
3. `run_sql`: Execute a read-only SQLite SELECT query. Argument: SQL query string.

Rules:
- You must NEVER execute destructive statements (DROP, DELETE, UPDATE, INSERT, ALTER).
- Always inspect the schema first if you do not know the exact column names.
- Always use the exact format below:

Thought: [Explain your reasoning]
Action: [tool_name: list_tables, describe_schema, or run_sql]
Action Input: [input to the tool]
Observation: [tool output will be provided here]

... (this Thought/Action/Action Input/Observation can repeat up to 5 times)

Thought: [Final rationale based on observations]
Final Answer: [Clear, comprehensive answer to the user question]

Begin!
Question: {question}
"""


class SQLReActAgent:
    """Autonomous ReAct agent for SQL database interaction."""

    def __init__(self, max_steps: int = 5):
        self.llm = get_llm()
        self.max_steps = max_steps
        self.tools = {
            "list_tables": lambda arg: tool_list_tables(),
            "describe_schema": lambda arg: tool_describe_schema(arg),
            "run_sql": lambda arg: tool_run_sql(arg)
        }

    def execute_tool(self, tool_name: str, tool_input: str) -> str:
        clean_name = tool_name.strip().lower()
        if clean_name not in self.tools:
            return f"Error: Tool '{tool_name}' is not recognized. Available tools: {list(self.tools.keys())}"
        
        try:
            return self.tools[clean_name](tool_input.strip())
        except Exception as e:
            return f"Tool execution exception: {str(e)}"

    def run(self, question: str) -> Dict[str, Any]:
        """Runs the ReAct loop."""
        # Destructive user intent guardrail fast-path
        is_safe, error = check_sql_safety(question)
        if not is_safe and ("drop" in question.lower() or "delete" in question.lower()):
            return {
                "question": question,
                "status": "BLOCKED_BY_GUARDRAIL",
                "steps": [{
                    "thought": "User requested destructive database action. Intercepting.",
                    "action": "GUARDRAIL_INTERCEPT",
                    "action_input": question,
                    "observation": error
                }],
                "final_answer": f"Refused to execute query. {error}"
            }

        steps: List[Dict[str, str]] = []

        if use_mock():
            # Generate realistic multi-step ReAct trace
            schema_obs = tool_describe_schema("customers")
            steps.append({
                "thought": "I need to find the top spending customers. First, let me inspect the schema of customers and orders tables.",
                "action": "describe_schema",
                "action_input": "customers",
                "observation": schema_obs
            })

            query = (
                "SELECT c.name, SUM(o.total_amount) AS total_spent "
                "FROM customers c "
                "JOIN orders o ON c.id = o.customer_id "
                "GROUP BY c.id ORDER BY total_spent DESC LIMIT 3;"
            )
            query_obs = tool_run_sql(query)
            steps.append({
                "thought": "Now that I have the column names, I can execute a JOIN query to sum order totals per customer.",
                "action": "run_sql",
                "action_input": query,
                "observation": query_obs
            })

            return {
                "question": question,
                "status": "COMPLETED",
                "steps": steps,
                "final_answer": (
                    "Based on database records, the top spending customers are:\n"
                    "1. Stark Industries ($25,000.00)\n"
                    "2. Umbrella Biotech ($18,499.00)\n"
                    "3. Wayne Enterprises ($15,999.00)"
                )
            }

        # Real ReAct loop
        scratchpad = ""
        prompt = REACT_SYSTEM_PROMPT.format(question=question)

        for step_idx in range(self.max_steps):
            current_prompt = prompt + scratchpad
            response = self.llm.invoke(current_prompt)
            output = getattr(response, "content", str(response))

            # Check for Final Answer
            if "Final Answer:" in output:
                final_answer = output.split("Final Answer:")[-1].strip()
                return {
                    "question": question,
                    "status": "COMPLETED",
                    "steps": steps,
                    "final_answer": final_answer
                }

            # Parse Thought, Action, Action Input
            thought_match = re.search(r'Thought:(.*?)(?=Action:|$)', output, re.DOTALL)
            action_match = re.search(r'Action:\s*([a-zA-Z_]+)', output)
            input_match = re.search(r'Action Input:(.*?)(?=Observation:|$)', output, re.DOTALL)

            thought = thought_match.group(1).strip() if thought_match else "Analyzing next step..."
            action = action_match.group(1).strip() if action_match else None
            action_input = input_match.group(1).strip() if input_match else ""

            if not action:
                # LLM didn't format action, finalize with content
                return {
                    "question": question,
                    "status": "COMPLETED",
                    "steps": steps,
                    "final_answer": output
                }

            # Execute tool
            obs = self.execute_tool(action, action_input)
            steps.append({
                "step": step_idx + 1,
                "thought": thought,
                "action": action,
                "action_input": action_input,
                "observation": obs
            })

            # Append to scratchpad
            scratchpad += f"\nThought: {thought}\nAction: {action}\nAction Input: {action_input}\nObservation: {obs}\n"

        return {
            "question": question,
            "status": "MAX_STEPS_REACHED",
            "steps": steps,
            "final_answer": "Agent reached maximum execution steps before finding a definitive answer."
        }
