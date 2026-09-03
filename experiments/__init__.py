"""
Experiments module loader.
Exposes clean Pythonic aliases for numbered experiment directories.
"""

import importlib

# Dynamic module loaders for numbered subpackages
def _load(module_path: str):
    return importlib.import_module(f"experiments.{module_path}")

# Module 01
mod_01_pipe = _load("01_text_to_sql.pipeline")
mod_01_val = _load("01_text_to_sql.schema_validator")
TextToSQLPipeline = mod_01_pipe.TextToSQLPipeline
SchemaValidator = mod_01_val.SchemaValidator

# Module 02
mod_02_qa = _load("02_rag_system.qa_chain")
mod_02_ingest = _load("02_rag_system.ingest")
mod_02_ret = _load("02_rag_system.retriever")
RAGSystem = mod_02_qa.RAGSystem
VectorIndexManager = mod_02_ingest.VectorIndexManager
SimpleTextChunker = mod_02_ingest.SimpleTextChunker
RAGRetriever = mod_02_ret.RAGRetriever
compute_term_overlap_score = mod_02_ret.compute_term_overlap_score

# Module 03
mod_03_chains = _load("03_prompt_chaining.chains")
PromptChainingSummarizer = mod_03_chains.PromptChainingSummarizer

# Module 04
mod_04_agent = _load("04_sql_react_agent.agent")
mod_04_guard = _load("04_sql_react_agent.guardrails")
mod_04_tools = _load("04_sql_react_agent.tools")
SQLReActAgent = mod_04_agent.SQLReActAgent
check_sql_safety = mod_04_guard.check_sql_safety
tool_list_tables = mod_04_tools.tool_list_tables
tool_describe_schema = mod_04_tools.tool_describe_schema

# Module 05
mod_05_crew = _load("05_multi_agent_sdr.crew")
mod_05_agents = _load("05_multi_agent_sdr.agents")
SDRMultiAgentWorkflow = mod_05_crew.SDRMultiAgentWorkflow
LeadGenerationAgent = mod_05_agents.LeadGenerationAgent
QualificationAgent = mod_05_agents.QualificationAgent
EmailingAgent = mod_05_agents.EmailingAgent

# Module 06
mod_06_eval = _load("06_policy_compliance.evaluator")
mod_06_rules = _load("06_policy_compliance.rules")
mod_06_data = _load("06_policy_compliance.synthetic_data")
PolicyComplianceAgent = mod_06_eval.PolicyComplianceAgent
run_deterministic_rules = mod_06_rules.run_deterministic_rules
get_synthetic_test_suite = mod_06_data.get_synthetic_test_suite

# Module 07
mod_07_wf = _load("07_deep_research_agent.workflow")
DeepResearchAgent = mod_07_wf.DeepResearchAgent

# Module 08
mod_08_pipe = _load("08_multimodal_vqa.pipeline")
mod_08_img = _load("08_multimodal_vqa.image_utils")
MultimodalVQAPipeline = mod_08_pipe.MultimodalVQAPipeline
image_to_base64 = mod_08_img.image_to_base64
generate_sample_diagram = mod_08_img.generate_sample_diagram

# Module 09
mod_09_bench = _load("09_reasoning_benchmark.benchmark")
mod_09_tasks = _load("09_reasoning_benchmark.tasks")
ReasoningBenchmarkHarness = mod_09_bench.ReasoningBenchmarkHarness
get_reasoning_tasks = mod_09_tasks.get_reasoning_tasks

# Module 10
mod_10_train = _load("10_finetuning_lora.train")
run_qlora_training = mod_10_train.run_qlora_training
calculate_lora_parameters = mod_10_train.calculate_lora_parameters

# Module 11
mod_11_bench = _load("11_model_optimization.benchmark")
ModelOptimizationBenchmark = mod_11_bench.ModelOptimizationBenchmark

# Module 12
mod_12_agent = _load("12_capstone_agent.agent")
CapstoneAgent = mod_12_agent.CapstoneAgent
