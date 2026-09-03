"""
AI Labs: Central Interactive Streamlit Dashboard
Interactive execution interface for all 12 Generative AI & Agentic Workflow experiments.
"""

import sys
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
from PIL import Image

# Import configuration and utilities
from src.config import (
    LLM_PROVIDER,
    DEFAULT_MODEL,
    OPENAI_API_KEY,
    use_mock,
    is_api_configured
)
from src.utils import get_schema_summary

# Import all 12 experiment modules via clean experiments package aliases
from experiments import (
    TextToSQLPipeline,
    RAGSystem,
    PromptChainingSummarizer,
    SQLReActAgent,
    SDRMultiAgentWorkflow,
    PolicyComplianceAgent,
    get_synthetic_test_suite,
    DeepResearchAgent,
    MultimodalVQAPipeline,
    generate_sample_diagram,
    ReasoningBenchmarkHarness,
    run_qlora_training,
    calculate_lora_parameters,
    ModelOptimizationBenchmark,
    CapstoneAgent
)


# ==============================================================================
# Page Configuration & Styling
# ==============================================================================
st.set_page_config(
    page_title="AI Labs | GenAI & Agentic Workflows",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern enterprise aesthetic
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #64748B;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .badge-success {
        background-color: #DCFCE7;
        color: #15803D;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-warning {
        background-color: #FEF3C7;
        color: #B45309;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-danger {
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# Sidebar Navigation & System Telemetry
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/circuit.png", width=60)
    st.markdown("### **AI Labs Navigation**")
    st.markdown("12 Production-Ready GenAI Experiments")

    experiment = st.selectbox(
        "Select Experiment Module:",
        [
            "01. Text-to-SQL Pipeline",
            "02. Grounded RAG QA System",
            "03. Prompt Chaining Summarizer",
            "04. SQL ReAct Agent with Guardrails",
            "05. Multi-Agent SDR System",
            "06. Policy Compliance Agent",
            "07. Deep Research Workflow",
            "08. Multimodal Visual QA",
            "09. Reasoning Model Benchmark",
            "10. Fine-Tuning Lab (QLoRA)",
            "11. Model Optimization & Quantization",
            "12. Capstone Multi-Tool Agent"
        ]
    )

    st.markdown("---")
    st.markdown("#### **Runtime Environment**")
    
    if is_api_configured():
        st.markdown(f'<span class="badge-success">● LIVE API ({LLM_PROVIDER.upper()})</span>', unsafe_allow_html=True)
        st.caption(f"Active Model: `{DEFAULT_MODEL}`")
    else:
        st.markdown('<span class="badge-warning">● SIMULATION / MOCK MODE</span>', unsafe_allow_html=True)
        st.caption("No API keys detected. Operating in deterministic offline mode.")

    st.markdown("---")
    st.markdown("#### **System Info**")
    st.caption("• Framework: LangChain / LangGraph / PEFT\n• Database: SQLite (Enterprise Demo)\n• Vector Index: Chroma / Semantic")


# ==============================================================================
# Header Section
# ==============================================================================
st.markdown('<div class="main-title">AI Labs: Generative AI & Agentic Workflows</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Production-grade implementations of 12 advanced AI agent patterns, retrieval systems, and model optimization techniques.</div>', unsafe_allow_html=True)


# ==============================================================================
# Module 01: Text-to-SQL Workflow
# ==============================================================================
if experiment.startswith("01"):
    st.header("Module 01: Enterprise Text-to-SQL Pipeline")
    st.markdown("Converts natural language queries into safe, verified SQLite statements with schema introspection and self-correction.")

    col1, col2 = st.columns([2, 1])
    with col1:
        user_query = st.text_input(
            "Natural Language Question:",
            value="Show me the top 3 customers by total spending."
        )
        if st.button("Generate & Execute SQL", type="primary"):
            with st.spinner("Generating, validating, and executing query..."):
                pipeline = TextToSQLPipeline()
                result = pipeline.generate_sql(user_query)

                st.success(f"Status: {result['status']} (Attempts: {result['attempts']})")
                st.code(result["sql"], language="sql")

                exec_data = result["execution"]
                if exec_data["success"]:
                    st.markdown(f"**Execution Output ({exec_data['row_count']} rows):**")
                    if exec_data["rows"]:
                        st.dataframe(pd.DataFrame(exec_data["rows"]), use_container_width=True)
                    else:
                        st.info("Query executed successfully, returning 0 rows.")
                else:
                    st.error(f"Execution Error: {exec_data.get('error')}")

    with col2:
        st.markdown("#### Database Schema")
        with st.expander("View Introspected Schema", expanded=True):
            st.text(get_schema_summary())


# ==============================================================================
# Module 02: RAG-Based Question Answering System
# ==============================================================================
elif experiment.startswith("02"):
    st.header("Module 02: Grounded RAG QA System")
    st.markdown("Context-augmented question answering with similarity retrieval and verifiable source citations.")

    col1, col2 = st.columns([2, 1])
    with col1:
        question = st.text_input(
            "Enter enterprise inquiry:",
            value="What are the enterprise security guidelines regarding PII and credit card numbers?"
        )
        if st.button("Retrieve & Synthesize Answer", type="primary"):
            with st.spinner("Searching document index and synthesizing answer..."):
                rag = RAGSystem()
                resp = rag.query(question)

                st.markdown("### Answer")
                st.markdown(resp["answer"])

                st.markdown("---")
                st.markdown("### Retrieved Citations & Passages")
                for s in resp["sources"]:
                    with st.expander(f"Source: {s['source']} (Score: {s['score']})"):
                        st.caption(f"Chunk Index: {s['chunk_index']}")
                        st.write(s["snippet"])

    with col2:
        st.markdown("#### Knowledge Corpus")
        st.info("Ingested Documents:\n- `agentic_workflows_overview.txt`\n- `enterprise_security_policy.txt`\n- `model_optimization_guide.txt`")


# ==============================================================================
# Module 03: Prompt Chaining for Summarization
# ==============================================================================
elif experiment.startswith("03"):
    st.header("Module 03: Multi-Stage Prompt Chaining Summarizer")
    st.markdown("Sequential decomposition: Key Points Extraction -> Thematic Chapter Synthesis -> Executive CTO Briefing.")

    default_text = (
        "Enterprise AI adoption has accelerated across finance and supply chain sectors. However, unstructured "
        "model deployments risk exposing Personally Identifiable Information (PII) and violating regulatory rules. "
        "Implementing ReAct-based agents allows teams to interleave verbal reasoning traces with atomic database tool "
        "invocations. Crucially, systems must enforce AST-based guardrails to block destructive SQL statements like "
        "DROP TABLE or DELETE. On the infrastructure side, 4-bit NormalFloat quantization (NF4) combined with LoRA "
        "reduces memory requirements by 78%, enabling fine-tuning on cost-effective GPUs without sacrificing model quality."
    )

    doc_input = st.text_area("Source Document for Analysis:", value=default_text, height=160)

    if st.button("Execute Prompt Chain", type="primary"):
        with st.spinner("Processing Stage 1, 2, and 3 chains..."):
            summarizer = PromptChainingSummarizer()
            res = summarizer.run(doc_input)

            tab1, tab2, tab3, tab4 = st.tabs([
                "Stage 1: Key Points",
                "Stage 2: Thematic Chapters",
                "Stage 3: Executive Summary",
                "Pipeline Telemetry"
            ])

            with tab1:
                st.markdown(res["stage_1_key_points"])
            with tab2:
                st.markdown(res["stage_2_chapter_summaries"])
            with tab3:
                st.markdown(res["stage_3_executive_summary"])
            with tab4:
                st.dataframe(pd.DataFrame(res["telemetry"]), use_container_width=True)
                st.metric("Total Execution Time", f"{res['total_duration_sec']}s")


# ==============================================================================
# Module 04: SQL Agent with Tool Use (ReAct)
# ==============================================================================
elif experiment.startswith("04"):
    st.header("Module 04: SQL Agent with Tool Use (ReAct Architecture)")
    st.markdown("Autonomous Reason + Act agent with database execution tools, schema inspection, and destructive query guardrails.")

    query_input = st.text_input(
        "Agent Data Goal / Query:",
        value="Which sales rep closed the highest revenue, and what was their quota?"
    )

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        run_normal = st.button("Run ReAct Agent", type="primary")
    with col_btn2:
        run_attack = st.button("⚠️ Test Destructive Injection Attack (`DROP TABLE customers`)")

    if run_normal or run_attack:
        target_q = "DROP TABLE customers;" if run_attack else query_input
        with st.spinner("Agent deliberating and invoking tools..."):
            agent = SQLReActAgent()
            result = agent.run(target_q)

            if result["status"] == "BLOCKED_BY_GUARDRAIL":
                st.error("🚨 " + result["final_answer"])
            else:
                st.success("Execution Completed")
                st.markdown("### Final Answer")
                st.markdown(result["final_answer"])

            st.markdown("---")
            st.markdown("### ReAct Thought-Action-Observation Trace")
            for idx, s in enumerate(result["steps"], 1):
                with st.expander(f"Step {idx}: Action `{s.get('action')}`", expanded=True):
                    st.markdown(f"**Thought:** {s.get('thought')}")
                    st.code(f"Input: {s.get('action_input')}\n\nObservation: {s.get('observation')}")


# ==============================================================================
# Module 05: Multi-Agent SDR System
# ==============================================================================
elif experiment.startswith("05"):
    st.header("Module 05: Multi-Agent SDR Outbound System")
    st.markdown("Coordinated crew: Lead Generation Agent -> ICP Qualification Agent -> Emailing Agent.")

    col1, col2 = st.columns(2)
    with col1:
        industry = st.text_input("Target Vertical / Industry:", value="Autonomous Supply Chain & Logistics")
    with col2:
        icp = st.text_input("ICP Criteria:", value="Enterprise >$200M revenue looking to adopt AI agents")

    value_prop = st.text_input(
        "Value Proposition:",
        value="Self-correcting AI pipelines with AST database security guardrails"
    )

    if st.button("Launch Multi-Agent Campaign", type="primary"):
        with st.spinner("Lead Gen Agent searching -> Qualification Agent scoring -> Emailing Agent drafting..."):
            sdr = SDRMultiAgentWorkflow()
            result = sdr.run_campaign(
                target_industry=industry,
                icp_criteria=icp,
                value_proposition=value_prop
            )

            p = result["prospect"]
            q = result["qualification"]
            e = result["outreach_email"]

            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown("#### 1. Lead Generation Profile")
                st.info(f"**Name:** {p.get('name')}\n\n**Title:** {p.get('title')}\n\n**Company:** {p.get('company')}\n\n**Revenue:** {p.get('estimated_revenue', '$450M')}")

            with c2:
                st.markdown("#### 2. ICP Qualification Score")
                score = q.get("icp_score", 90)
                st.metric("ICP Fit Score", f"{score}/100", delta="High Intent")
                st.markdown(f"**Fit Status:** `{q.get('fit_status', 'QUALIFIED')}`")

            st.markdown("---")
            st.markdown("#### 3. Personalized Outbound Email Draft")
            st.text_input("Subject:", value=e.get("subject", ""), disabled=True)
            st.text_area("Email Body:", value=e.get("body", ""), height=220, disabled=True)


# ==============================================================================
# Module 06: Policy Compliance Agent
# ==============================================================================
elif experiment.startswith("06"):
    st.header("Module 06: Enterprise Policy Compliance Agent")
    st.markdown("Two-tier audit combining deterministic regex scanners with semantic LLM judging for PII, financial, and regulatory risk.")

    synthetic_tests = get_synthetic_test_suite()
    sample_options = [f"{tc['id']} ({tc['label']}) - {tc['violation_type']}" for tc in synthetic_tests]
    selected_sample = st.selectbox("Load Synthetic Benchmark Sample:", ["Custom Input"] + sample_options)

    if selected_sample != "Custom Input":
        idx = int(selected_sample.split()[0].replace("TC-0", "").replace("TC-", "")) - 1
        default_val = synthetic_tests[idx]["text"]
    else:
        default_val = "Customer refund requested. Send confirmation to tony@stark.org. Payment card 4111 2222 3333 4444."

    audit_text = st.text_area("Text to Audit for Policy Violations:", value=default_val, height=120)

    if st.button("Run Compliance Audit", type="primary"):
        with st.spinner("Scanning deterministic rules and running LLM judge..."):
            agent = PolicyComplianceAgent()
            report = agent.evaluate(audit_text)

            c1, c2 = st.columns([1, 2])
            with c1:
                score = report["risk_score"]
                st.metric("Compliance Risk Score", f"{score}/100")
                if report["is_compliant"]:
                    st.markdown('<span class="badge-success">STATUS: PASS</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-danger">STATUS: FLAGGED</span>', unsafe_allow_html=True)

            with c2:
                st.markdown("#### Rule Violations")
                if report["deterministic_violations"]:
                    for v in report["deterministic_violations"]:
                        st.error(f"**[{v['severity']}] {v['name']}**: Found matches {v['matches']}")
                        st.caption(f"Remediation: {v['remediation']}")
                else:
                    st.success("No deterministic regex policy violations detected.")

            st.markdown("---")
            st.markdown("#### LLM Auditor Analysis")
            st.write(report["llm_audit_summary"])


# ==============================================================================
# Module 07: Deep Research Agent Workflow
# ==============================================================================
elif experiment.startswith("07"):
    st.header("Module 07: Deep Research Agent Workflow")
    st.markdown("Iterative Plan -> Execute -> Reflect -> Refine research workflow with multi-query evidence gathering and final dossier synthesis.")

    topic = st.text_input(
        "Research Investigation Topic:",
        value="Post-training quantization techniques (INT8 vs NF4) for edge LLM deployment"
    )

    if st.button("Execute Deep Research Loop", type="primary"):
        with st.spinner("Executing iterative research and reflection cycles..."):
            researcher = DeepResearchAgent(max_iterations=2)
            result = researcher.run(topic)

            st.success(f"Research Completed ({result['total_evidence_pieces']} pieces of evidence analyzed)")

            tab1, tab2, tab3 = st.tabs(["Final Research Dossier", "Iterations & Reflection", "Research Plan"])

            with tab1:
                st.markdown(result["final_report"])

            with tab2:
                for it in result["iterations"]:
                    with st.expander(f"Iteration {it['iteration']}: {it['queries_executed']}", expanded=True):
                        st.markdown(f"**Findings Gathered:** {it['findings_count']}")
                        st.info(it["reflection"])

            with tab3:
                for idx, step in enumerate(result["research_plan"], 1):
                    st.markdown(f"{idx}. {step}")


# ==============================================================================
# Module 08: Multimodal Visual QA System
# ==============================================================================
elif experiment.startswith("08"):
    st.header("Module 08: Multimodal Visual QA System")
    st.markdown("Combines Vision-LLMs with ground-truth textual enterprise documentation to analyze diagrams, charts, and schematics.")

    c1, c2 = st.columns([1, 1])
    sample_diagram = generate_sample_diagram()

    with c1:
        st.markdown("#### Input Architecture Diagram")
        st.image(sample_diagram, caption="Enterprise AI Gateway Architecture", use_column_width=True)

    with c2:
        st.markdown("#### Visual Inquiry")
        vqa_question = st.text_input(
            "Ask a question about the diagram:",
            value="What components sit between the client application and the foundation model, and what is the SLA?"
        )

        if st.button("Analyze Image & Context", type="primary"):
            with st.spinner("Encoding image and querying Vision-LLM..."):
                vqa = MultimodalVQAPipeline()
                res = vqa.analyze_image(image=sample_diagram, question=vqa_question)

                st.markdown("### Analysis Result")
                st.markdown(res["answer"])

                if res.get("visual_elements_detected"):
                    st.caption("Visual Entities Identified: " + ", ".join(res["visual_elements_detected"]))


# ==============================================================================
# Module 09: Reasoning Model Benchmarking
# ==============================================================================
elif experiment.startswith("09"):
    st.header("Module 09: Reasoning Model Benchmarking Suite")
    st.markdown("Profiles Zero-Shot, Few-Shot, Chain-of-Thought (CoT), and Tree-of-Thought (ToT) strategies across complex reasoning tasks.")

    if st.button("Run Reasoning Benchmark Suite", type="primary"):
        with st.spinner("Benchmarking prompting strategies across reasoning tasks..."):
            harness = ReasoningBenchmarkHarness()
            results = harness.run_benchmark()

            st.markdown("### Comparative Performance Matrix")
            st.dataframe(results["summary_df"], use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Accuracy Comparison (%)")
                st.bar_chart(data=results["summary_df"].set_index("strategy")["accuracy_pct"])

            with c2:
                st.markdown("#### Latency Comparison (seconds)")
                st.bar_chart(data=results["summary_df"].set_index("strategy")["avg_latency_sec"])

            st.markdown("---")
            st.markdown("#### Detailed Task Executions")
            st.dataframe(results["raw_df"][["task_id", "strategy", "latency_sec", "correct", "output_preview"]], use_container_width=True)


# ==============================================================================
# Module 10: Fine-Tuning Lab (QLoRA)
# ==============================================================================
elif experiment.startswith("10"):
    st.header("Module 10: Fine-Tuning for Domain Adaptation (PEFT / QLoRA)")
    st.markdown("Parameter-Efficient Fine-Tuning using 4-bit NormalFloat quantization and Low-Rank Adaptation (LoRA).")

    c1, c2, c3 = st.columns(3)
    with c1:
        rank = st.slider("LoRA Rank (r):", min_value=4, max_value=64, value=16, step=4)
    with c2:
        alpha = st.slider("LoRA Alpha:", min_value=8, max_value=128, value=32, step=8)
    with c3:
        quant_mode = st.selectbox("Base Quantization:", ["4-bit NormalFloat (NF4)", "8-bit (LLM.int8)", "16-bit (FP16)"])

    stats = calculate_lora_parameters(rank=rank)

    colA, colB, colC = st.columns(3)
    colA.metric("Base Model Parameters", "7.0 Billion")
    colB.metric("Trainable LoRA Parameters", f"{stats['trainable_lora_parameters']:,}")
    colC.metric("Parameter Reduction", stats["parameter_reduction_ratio"])

    if st.button("Run QLoRA Training Simulation", type="primary"):
        with st.spinner("Loading base weights, attaching LoRA adapters, executing training loop..."):
            training_result = run_qlora_training(dry_run=True)

            st.success("QLoRA Training Run Complete!")
            
            c_mem1, c_mem2 = st.columns(2)
            with c_mem1:
                st.metric("Estimated GPU VRAM Needed", f"{training_result['estimated_vram_gb']} GB", delta="-77.8% vs FP16", delta_color="inverse")
            with c_mem2:
                st.metric("Final Training Loss", f"{training_result['final_loss']}")

            st.markdown("#### Training Loss Curve")
            loss_df = pd.DataFrame(training_result["training_log"])
            st.line_chart(data=loss_df.set_index("step")["loss"])


# ==============================================================================
# Module 11: Model Optimization Lab
# ==============================================================================
elif experiment.startswith("11"):
    st.header("Module 11: Model Optimization & Quantization Lab")
    st.markdown("Systematic hardware and fidelity profiling across FP16, INT8 (LLM.int8), and INT4 (NF4) quantization regimes.")

    tokens_gen = st.slider("Tokens to Generate for Latency Test:", 64, 512, 128, step=64)

    if st.button("Profile Quantization Precision Modes", type="primary"):
        with st.spinner("Measuring memory, latency, and perplexity..."):
            bench = ModelOptimizationBenchmark()
            data = bench.run_benchmark_suite(tokens_to_generate=tokens_gen)
            df = data["results_table"]

            st.dataframe(df, use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Generation Throughput (tokens/second)")
                st.bar_chart(df.set_index("Precision Mode")["Throughput (tok/s)"])
            with c2:
                st.markdown("#### Memory Footprint (VRAM GB)")
                st.bar_chart(df.set_index("Precision Mode")["Min VRAM (GB)"])


# ==============================================================================
# Module 12: Mini Project (Capstone) - Agentic Multi-Tool RAG System
# ==============================================================================
elif experiment.startswith("12"):
    st.header("Module 12: Mini Project (Capstone) — Agentic Multi-Tool RAG")
    st.markdown("End-to-end supervisor agent combining Relational Text-to-SQL, Semantic RAG, and Real-Time Policy Compliance.")

    sample_capstone_queries = [
        "Which enterprise customer spent the most, and what is our policy regarding PII in customer outputs?",
        "Show me all products with price greater than $3000.",
        "What are the ground-truth hallucination controls in our RAG systems?"
    ]
    selected_q = st.selectbox("Sample Inquiries:", ["Custom Query"] + sample_capstone_queries)

    if selected_q != "Custom Query":
        input_q = selected_q
    else:
        input_q = "List our top 3 customers by revenue and verify if the response is compliant with data privacy rules."

    capstone_query = st.text_input("Enterprise Multi-Tool Inquiry:", value=input_q)

    if st.button("Execute Multi-Tool Agent", type="primary"):
        with st.spinner("Supervisor analyzing intent, invoking tools, and auditing compliance..."):
            agent = CapstoneAgent()
            res = agent.run(capstone_query)

            st.markdown("### Integrated Synthesis")
            st.markdown(res["final_answer"])

            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            c1.metric("Classified Intent", res["intent"])
            c2.metric("Execution Latency", f"{res['latency_sec']}s")
            c3.metric("Compliance Status", res["compliance"]["status"])

            st.markdown("### Agent Execution Trace")
            for trace_item in res["execution_trace"]:
                st.markdown(f"- {trace_item}")
