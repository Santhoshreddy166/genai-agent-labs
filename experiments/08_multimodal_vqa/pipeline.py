"""
Multimodal Visual QA Pipeline combining Vision LLMs with ground-truth textual context.
"""

from typing import Dict, Any, Optional
from PIL import Image
from src.config import use_mock, OPENAI_API_KEY
from src.utils import logger
from .image_utils import image_to_base64, generate_sample_diagram
from .context_retriever import MultimodalContextRetriever


class MultimodalVQAPipeline:
    """Answers user queries regarding image diagrams augmented with text context."""

    def __init__(self):
        self.context_retriever = MultimodalContextRetriever()

    def analyze_image(
        self,
        image: Optional[Image.Image] = None,
        question: str = "Explain the architecture and the latency SLA shown in this diagram."
    ) -> Dict[str, Any]:
        """
        Executes Multimodal VQA on the supplied image or sample diagram.
        """
        target_img = image or generate_sample_diagram()
        img_b64 = image_to_base64(target_img)

        # Retrieve text context related to question
        context_chunks = self.context_retriever.get_context_for_query(question)
        context_text = "\n".join([f"- {c['content'][:150]}" for c in context_chunks])

        if use_mock() or not OPENAI_API_KEY:
            # Deterministic analysis for demo/offline
            return {
                "question": question,
                "status": "SUCCESS (MOCK)",
                "visual_elements_detected": [
                    "Header banner: Enterprise AI Gateway Architecture",
                    "Three pipeline stages: Client Application -> AST Guardrail & Security Layer -> Foundation Model",
                    "Status metrics: Latency SLA < 450ms, Guardrail Pass Rate 99.8%"
                ],
                "answer": (
                    "Based on the visual diagram and enterprise context:\n"
                    "1. Architecture Flow: Incoming client requests pass through a dedicated AST Security Guardrail "
                    "layer before reaching the underlying Foundation Model (GPT-4o / QLoRA).\n"
                    "2. Operational SLA: The architecture mandates an end-to-end latency SLA under 450ms and maintains "
                    "a 99.8% guardrail pass rate.\n"
                    "3. Alignment: This matches enterprise security policies requiring pre-inference sanitization."
                ),
                "context_used": context_chunks
            }

        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import HumanMessage

            llm = ChatOpenAI(model="gpt-4o", max_tokens=600)
            message = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": (
                            f"Answer the following question about the attached image.\n"
                            f"Additional enterprise context:\n{context_text}\n\n"
                            f"Question: {question}"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": img_b64}
                    }
                ]
            )
            response = llm.invoke([message])
            answer_text = response.content

            return {
                "question": question,
                "status": "SUCCESS",
                "visual_elements_detected": ["Image parsed via GPT-4o Vision API"],
                "answer": answer_text,
                "context_used": context_chunks
            }
        except Exception as e:
            logger.error(f"Multimodal QA call failed: {e}. Falling back to simulation.")
            return {
                "question": question,
                "status": "ERROR_FALLBACK",
                "answer": f"Analysis based on visual structure: The diagram illustrates a secure 3-tier gateway with an AST Guardrail layer enforcing < 450ms SLA.",
                "context_used": context_chunks
            }
