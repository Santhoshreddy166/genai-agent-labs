"""
Image utilities for Multimodal Visual QA.
Handles loading, base64 encoding, and programmatic test image generation.
"""

import io
import base64
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont


def image_to_base64(image_path_or_pil) -> str:
    """Converts a PIL image or image file path to a base64 data URL string."""
    if isinstance(image_path_or_pil, (str, Path)):
        img = Image.open(str(image_path_or_pil))
    else:
        img = image_path_or_pil

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"


def generate_sample_diagram(output_path: Optional[Path] = None) -> Image.Image:
    """Generates a clean synthetic architecture diagram image for zero-dependency testing."""
    width, height = 600, 320
    img = Image.new("RGB", (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    # Title box
    draw.rectangle([20, 20, 580, 60], fill=(30, 41, 59), outline=(15, 23, 42))
    draw.text((35, 30), "Enterprise AI Gateway Architecture", fill=(255, 255, 255))

    # Boxes
    # 1. User App
    draw.rectangle([40, 100, 180, 180], fill=(59, 130, 246), outline=(29, 78, 216))
    draw.text((55, 130), "Client Application\n(Streamlit / UI)", fill=(255, 255, 255))

    # 2. Guardrail Engine
    draw.rectangle([230, 100, 370, 180], fill=(16, 185, 129), outline=(4, 120, 87))
    draw.text((245, 130), "AST Guardrail &\nSecurity Layer", fill=(255, 255, 255))

    # 3. Model Engine
    draw.rectangle([420, 100, 560, 180], fill=(139, 92, 246), outline=(109, 40, 217))
    draw.text((435, 130), "Foundation Model\n(GPT-4o / QLoRA)", fill=(255, 255, 255))

    # Connectors
    draw.line([(180, 140), (230, 140)], fill=(71, 85, 105), width=3)
    draw.line([(370, 140), (420, 140)], fill=(71, 85, 105), width=3)

    # Bottom status banner
    draw.rectangle([40, 230, 560, 280], fill=(226, 232, 240), outline=(203, 213, 225))
    draw.text((60, 248), "Latency SLA: < 450ms | Guardrail Pass Rate: 99.8%", fill=(51, 65, 85))

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path))

    return img
