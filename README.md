# ⚡ AI Labs: Enterprise Generative AI & Agentic Workflows

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain%20%7C%20LangGraph-1C3C3C.svg)](https://langchain.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![PEFT](https://img.shields.io/badge/Fine--Tuning-PEFT%20%2F%20QLoRA-yellow.svg)](https://github.com/huggingface/peft)
[![Docker](https://img.shields.io/badge/Deployment-Docker%20Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

A modular, production-ready, open-source-grade Python monorepo showcasing **12 advanced Generative AI and Agentic Workflow experiments**. Includes safe Text-to-SQL with self-correction, Grounded RAG with source attribution, Multi-Agent SDR crews, ReAct agents with AST guardrails, Vision QA, PEFT QLoRA fine-tuning, quantization benchmarking, and a unified Capstone Agent dashboard.

---

## 📑 Table of Contents
- [System Architecture](#-system-architecture)
- [Repository Structure](#-repository-structure)
- [The 12 Experiment Modules](#-the-12-experiment-modules)
- [Quickstart Guide](#-quickstart-guide)
- [Running Tests](#-running-tests)
- [Interactive UI Dashboard](#-interactive-ui-dashboard)
- [Deployment Guide](#-deployment-guide)
  - [Hugging Face Spaces](#1-hugging-face-spaces)
  - [Streamlit Community Cloud](#2-streamlit-community-cloud)
  - [Docker Container](#3-docker-container)
- [Contributing & License](#-contributing--license)

---

## 🏛 System Architecture

```
                                  USER INTERFACE (Streamlit / API)
                                                │
                                                ▼
                            ┌───────────────────────────────────────┐
                            │     Central Config & LLM Factory      │
                            │ (OpenAI / Anthropic / Local Fallback) │
                            └───────────────────┬───────────────────┘
                                                │
                        ┌───────────────────────┴───────────────────────┐
                        ▼                                               ▼
         ┌───────────────────────────────┐              ┌───────────────────────────────┐
         │     Agentic Orchestration     │              │    Data & Model Systems       │
         │  • ReAct SQL Agent (04)       │              │  • SQLite Enterprise DB       │
         │  • Multi-Agent SDR Crew (05)  │              │  • Chroma Vector DB (02)      │
         │  • Deep Research Agent (07)   │              │  • QLoRA PEFT Adapters (10)   │
         │  • Capstone Supervisor (12)   │              │  • Quantization Engine (11)   │
         └──────────────┬────────────────┘              └───────────────┬───────────────┘
                        │                                               │
                        └───────────────────────┬───────────────────────┘
                                                ▼
                            ┌───────────────────────────────────────┐
                            │    AST Security & Policy Guardrails   │
                            │  • Destructive SQL Interception       │
                            │  • PII & Regulatory Audit (06)        │
                            └───────────────────┬───────────────────┘
                                                │
                                                ▼
                                    AUDIT-VERIFIED RESPONSE
```

---

## 📂 Repository Structure

```
ai-labs/
├── README.md                      # Comprehensive project guide & documentation
├── requirements.txt               # Pinned Python package dependencies
├── .env.example                   # Environment credential template
├── Dockerfile                     # Cloud & container deployment spec
├── .gitignore                     # Git ignore rules
├── app.py                         # Central Streamlit Interactive Dashboard
├── data/                          # Data store directory
│   ├── seed_data.py               # Seeds enterprise SQLite DB & knowledge documents
│   ├── enterprise_demo.db         # Demo SQLite database
│   └── documents/                 # Sample knowledge base texts (.txt)
├── src/
│   ├── config.py                  # Environment loader & provider configurations
│   └── utils.py                   # LLM factory, DB connections, mock fallbacks
├── experiments/
│   ├── __init__.py                # Package exposing clean module aliases
│   ├── 01_text_to_sql/            # NL-to-SQL with schema self-correction
│   ├── 02_rag_system/             # Document chunking, retrieval & grounded QA
│   ├── 03_prompt_chaining/        # 3-stage summarization pipeline
│   ├── 04_sql_react_agent/        # ReAct agent with DB tools & guardrails
│   ├── 05_multi_agent_sdr/        # Lead Gen -> Qualification -> Emailing crew
│   ├── 06_policy_compliance/      # Deterministic & LLM-judge compliance audit
│   ├── 07_deep_research_agent/    # Plan + Execute + Reflect + Refine loop
│   ├── 08_multimodal_vqa/         # Vision-LLM diagram analysis + RAG context
│   ├── 09_reasoning_benchmark/    # Zero-Shot, Few-Shot, CoT, ToT comparison
│   ├── 10_finetuning_lora/        # QLoRA (NF4) PEFT fine-tuning script
│   ├── 11_model_optimization/     # FP16 vs INT8 vs INT4 latency & VRAM lab
│   └── 12_capstone_agent/         # Unified Supervisor Multi-Tool Agent
└── tests/                         # Pytest test suite (16 automated tests)
    ├── test_01_text_to_sql.py
    ├── test_02_rag_qa.py
    ├── test_03_prompt_chaining.py
    ├── test_04_sql_agent.py
    ├── test_06_policy_compliance.py
    └── test_09_reasoning_benchmark.py
```

---

## 🔬 The 12 Experiment Modules

| # | Module | Core Framework / Technique | Key Feature |
|---|---|---|---|
| **01** | **Text-to-SQL Pipeline** | SQLite, AST Parsing | Schema introspection with an automated 3-attempt self-correction loop. |
| **02** | **Grounded RAG System** | Chunking, Similarity Retrieval | Source attribution with document passage metadata and cosine thresholds. |
| **03** | **Prompt Chaining** | Sequential Prompts | Key Points -> Thematic Chapter Synthesis -> Executive CTO Briefing. |
| **04** | **SQL ReAct Agent** | Reason + Act, AST Guardrails | Intercepts destructive queries (`DROP`, `DELETE`) before execution. |
| **05** | **Multi-Agent SDR System** | Autonomous Crews | 3 specialized agents: Lead Generation, ICP Qualification, Email Outreach. |
| **06** | **Policy Compliance Agent** | Regex + LLM Judge | Scans for PII (emails, credit cards), regulatory risk, and financial promises. |
| **07** | **Deep Research Workflow** | Plan-Execute-Reflect-Refine | Iterative research cycles identifying evidence gaps and compiling dossiers. |
| **08** | **Multimodal Visual QA** | Vision-Language Models | Analyzes architecture diagrams, extracting entities and verifying against SLAs. |
| **09** | **Reasoning Benchmarking** | Prompt Engineering | Evaluates Zero-Shot, Few-Shot, CoT, and Tree-of-Thought (ToT) strategies. |
| **10** | **Fine-Tuning (QLoRA)** | Hugging Face PEFT, NF4 | Parameter-efficient adaptation reducing trainable weights by **99.76%**. |
| **11** | **Model Optimization** | Quantization Profiling | Compares FP16, INT8, and INT4 across latency, throughput, and perplexity. |
| **12** | **Capstone Agent** | Multi-Tool Supervisor | Routes queries dynamically between Relational SQL, RAG, and Compliance filters. |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (Python 3.10 – 3.13 supported)
- Git

### 2. Clone and Setup Environment
```bash
git clone https://github.com/your-username/ai-labs.git
cd ai-labs

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Credentials (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your `OPENAI_API_KEY` (or Anthropic/Google keys). 
> **Zero-Dependency Guarantee**: If no API key is provided, the repository automatically runs in **Deterministic Simulation / Mock Mode**, allowing full offline exploration and testing without API costs!

### 4. Seed Database & Documents
```bash
python data/seed_data.py
```

### 5. Launch the Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Tests

Execute the automated test suite covering safety guardrails, RAG retrieval, prompt chaining, and reasoning benchmarks:

```bash
pytest -v
```

All 16 unit tests run cleanly without external network calls.

---

## 💻 Interactive UI Dashboard (`app.py`)

The root `app.py` provides an interactive web interface with:
- **Runtime Environment Indicator**: Displays whether the app is running in **LIVE API** or **SIMULATION** mode.
- **Interactive Execution**: Test live queries, destructive injections, file uploads, and hyperparameter sliders.
- **Visual Analytics**: Interactive performance bar charts, latency timelines, and loss curves.

---

## 🌐 Deployment Guide

### 1. Hugging Face Spaces
1. Create a new **Streamlit Space** on [Hugging Face Spaces](https://huggingface.co/spaces).
2. Set the repository files to this project.
3. In **Settings -> Variables and Secrets**, add `OPENAI_API_KEY` (optional).
4. Hugging Face automatically detects `requirements.txt` and boots `app.py`.

### 2. Streamlit Community Cloud
1. Push the repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Connect your repository and select `app.py` as the Main file path.
4. In Advanced Settings, add your environment secrets from `.env.example`.
5. Click **Deploy**.

### 3. Docker Container
Deploy anywhere using the included multi-stage Docker container:

```bash
# Build Docker image
docker build -t ai-labs:latest .

# Run container on port 8501
docker run -p 8501:8501 -e OPENAI_API_KEY="your-key" ai-labs:latest
```

---

## 📄 License
Distributed under the **Apache 2.0 License**. See `LICENSE` for more information.
