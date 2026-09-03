"""
Database and sample document seeder for AI Labs.
Generates an SQLite enterprise database and sample knowledge base documents.
"""

import os
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
DB_PATH = DATA_DIR / "enterprise_demo.db"
DOCS_DIR = DATA_DIR / "documents"


def seed_database():
    """Create and seed the demo SQLite database."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 1. Customers Table
    cursor.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        country TEXT NOT NULL,
        tier TEXT CHECK(tier IN ('Enterprise', 'Mid-Market', 'Startup')),
        signup_date DATE NOT NULL
    );
    """)

    customers_data = [
        ("Acme Corp", "contact@acme.com", "USA", "Enterprise", "2023-01-15"),
        ("Globex Corporation", "billing@globex.net", "UK", "Enterprise", "2023-02-20"),
        ("Soylent Health", "info@soylent.org", "Germany", "Mid-Market", "2023-04-10"),
        ("Initech Systems", "peter@initech.io", "USA", "Startup", "2023-06-01"),
        ("Umbrella Biotech", "ops@umbrella.corp", "Japan", "Enterprise", "2023-07-22"),
        ("Hooli Tech", "gavin@hooli.com", "USA", "Enterprise", "2023-08-05"),
        ("Massive Dynamic", "walter@massivedynamic.com", "USA", "Enterprise", "2023-09-12"),
        ("Stark Industries", "tony@stark.org", "USA", "Enterprise", "2023-10-01"),
        ("Wayne Enterprises", "bruce@waynecorp.com", "USA", "Enterprise", "2023-10-18"),
        ("Cyberdyne Systems", "miles@cyberdyne.ai", "Canada", "Mid-Market", "2023-11-25"),
    ]
    cursor.executemany("INSERT INTO customers (name, email, country, tier, signup_date) VALUES (?, ?, ?, ?, ?)", customers_data)

    # 2. Products Table
    cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    );
    """)

    products_data = [
        ("SKU-AI-01", "Enterprise LLM Gateway", "Software", 4999.00, 100),
        ("SKU-AI-02", "Vector Database Cloud License", "Infrastructure", 1200.00, 50),
        ("SKU-AI-03", "Autonomous Agent Orchestrator", "Software", 3500.00, 80),
        ("SKU-SEC-01", "Compliance Guardrail Suite", "Security", 2400.00, 120),
        ("SKU-HW-01", "Edge AI Inference Node", "Hardware", 850.00, 30),
        ("SKU-SRV-01", "Dedicated Model Fine-tuning Cluster", "Services", 12500.00, 10),
    ]
    cursor.executemany("INSERT INTO products (sku, name, category, price, stock_quantity) VALUES (?, ?, ?, ?, ?)", products_data)

    # 3. Orders Table
    cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date DATE NOT NULL,
        status TEXT CHECK(status IN ('Completed', 'Pending', 'Cancelled')),
        total_amount REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );
    """)

    orders_data = [
        (1, "2024-01-10", "Completed", 9998.00),
        (1, "2024-02-15", "Completed", 3500.00),
        (2, "2024-01-20", "Completed", 12500.00),
        (3, "2024-03-05", "Completed", 2400.00),
        (4, "2024-03-12", "Pending", 1200.00),
        (5, "2024-03-22", "Completed", 18499.00),
        (6, "2024-04-01", "Completed", 4999.00),
        (7, "2024-04-18", "Cancelled", 3500.00),
        (8, "2024-05-02", "Completed", 25000.00),
        (9, "2024-05-14", "Completed", 15999.00),
        (10, "2024-05-20", "Completed", 2050.00),
    ]
    cursor.executemany("INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (?, ?, ?, ?)", orders_data)

    # 4. Sales Reps Table
    cursor.execute("""
    CREATE TABLE sales_reps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        region TEXT NOT NULL,
        quota REAL NOT NULL,
        closed_revenue REAL NOT NULL
    );
    """)

    reps_data = [
        ("Alice Cooper", "North America", 100000.00, 115000.00),
        ("Bob Martinez", "EMEA", 80000.00, 72000.00),
        ("Carol Chen", "APAC", 90000.00, 105000.00),
        ("David Smith", "LATAM", 60000.00, 45000.00),
    ]
    cursor.executemany("INSERT INTO sales_reps (name, region, quota, closed_revenue) VALUES (?, ?, ?, ?)", reps_data)

    # 5. Compliance Policies Table
    cursor.execute("""
    CREATE TABLE compliance_policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_code TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT CHECK(severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW'))
    );
    """)

    policies_data = [
        ("POL-SEC-01", "Data Privacy", "All customer Personally Identifiable Information (PII) including email, phone, and card details must be masked before model transmission.", "CRITICAL"),
        ("POL-FIN-02", "Financial Representation", "Outputs must not guarantee investment returns, stock predictions, or make unwarranted financial commitments.", "HIGH"),
        ("POL-ETH-03", "Content Moderation", "No harassment, hate speech, biased stereotyping, or derogatory remarks regarding protected classes.", "CRITICAL"),
        ("POL-OPS-04", "Database Safety", "Destructive operations (DROP, DELETE, ALTER, TRUNCATE) are forbidden via automated user endpoints.", "CRITICAL"),
    ]
    cursor.executemany("INSERT INTO compliance_policies (policy_code, category, description, severity) VALUES (?, ?, ?, ?)", policies_data)

    conn.commit()
    conn.close()
    print(f"[OK] Database seeded successfully at: {DB_PATH}")


def seed_documents():
    """Create sample knowledge base documents for RAG systems."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    doc_1 = DOCS_DIR / "agentic_workflows_overview.txt"
    doc_1.write_text("""
Title: Engineering Autonomous AI Agents: Architecture & Patterns

1. Overview
Modern Generative AI has transitioned from single-prompt stateless completions to stateful agentic workflows. An AI Agent combines a core Reasoning Engine (LLM), Memory (short-term conversational context and long-term vector embeddings), Planning (decomposition and reflection), and Tool Use (APIs, databases, and code execution environments).

2. The ReAct Pattern
The Reason + Act (ReAct) paradigm interleaves verbal reasoning traces with task-specific actions. Instead of guessing an answer directly, the agent:
- Generates a 'Thought' explaining its logical step.
- Emits an 'Action' selecting a registered tool and its arguments.
- Receives an 'Observation' with the raw tool output.
- Repeats until a final synthesized answer is reached.

3. Guardrails and Safety
Autonomous agents with tool access represent operational risk if left unconstrained. Crucial architectural requirements include:
- Execution boundaries: Read-only database views and parameter whitelisting.
- Human-in-the-loop triggers for high-stakes actions (financial transfers, outbound communications).
- Strict output validation and deterministic schema parsing.
""", encoding="utf-8")

    doc_2 = DOCS_DIR / "enterprise_security_policy.txt"
    doc_2.write_text("""
Enterprise AI Security and Governance Policy (v3.2)

1. Data Classification and PII Sanitization
Under GDPR, CCPA, and internal data handling directives, no prompt sent to third-party Foundation Model endpoints may contain cleartext PII (Personally Identifiable Information), including Social Security Numbers, Customer Payment Details, or Personal Email Addresses. All ingestion pipelines must apply deterministic tokenization or regex redaction prior to vector indexing.

2. SQL and Database Protection
Automated NL-to-SQL workflows and ReAct agents must operate strictly within least-privilege database connections. DDL (Data Definition Language) commands such as DROP TABLE, ALTER TABLE, or TRUNCATE TABLE, and bulk DML operations (DELETE, UPDATE) without verified tenant WHERE clauses are prohibited and must be intercepted by AST inspection guardrails.

3. Hallucination Controls in RAG Systems
To avoid misleading stakeholders, RAG pipelines must implement ground-truth verification. If retrieved similarity scores fall below the configurable threshold (default: cosine distance > 0.45), the model must state that insufficient verified enterprise context exists rather than extrapolating.
""", encoding="utf-8")

    doc_3 = DOCS_DIR / "model_optimization_guide.txt"
    doc_3.write_text("""
Quantization and Parameter-Efficient Fine-Tuning (PEFT) Guide

1. Post-Training Quantization (PTQ)
Deploying large language models (LLMs) in production often encounters severe memory bandwidth bottlenecks. Quantization compresses weights from FP16 (16-bit floating point) to INT8 or INT4 representations:
- INT8 (LLM.int8()): Employs vector-wise scaling to preserve outlier activations, typically yielding a 50% memory reduction with negligible perplexity degradation.
- INT4 (NF4 - NormalFloat4): Used extensively in QLoRA, representing weights with optimal theoretical information density for zero-mean normal distributions.

2. Parameter-Efficient Fine-Tuning (PEFT / LoRA)
Low-Rank Adaptation (LoRA) freezes the pre-trained model weights and injects trainable rank decomposition matrices into each transformer layer (such as the query and value projection matrices). This slashes the number of trainable parameters by up to 99% while achieving performance parity with full parameter fine-tuning.
""", encoding="utf-8")

    print(f"[OK] Sample documents generated at: {DOCS_DIR}")


if __name__ == "__main__":
    seed_database()
    seed_documents()
