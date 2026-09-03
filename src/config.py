"""
Central configuration module for AI Labs.
Loads environment variables, handles provider configuration, and provides fallbacks.
"""

import os
from pathlib import Path

# Base paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = DATA_DIR / "documents"
EXPERIMENTS_DIR = ROOT_DIR / "experiments"

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=ROOT_DIR / ".env")
except ImportError:
    pass

# Provider Settings
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")

# Databases
SQLITE_DB_PATH = Path(os.getenv("SQLITE_DB_PATH", DATA_DIR / "enterprise_demo.db"))
CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", DATA_DIR / "chroma_db"))

# Operational Mode
# If True or if no API keys are configured, fallback to offline deterministic simulation
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() in ("true", "1", "yes")

def is_api_configured() -> bool:
    """Check if any valid LLM API key is present."""
    if LLM_PROVIDER == "openai" and OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-proj-your"):
        return True
    if LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY and not ANTHROPIC_API_KEY.startswith("your-"):
        return True
    if LLM_PROVIDER == "google" and GOOGLE_API_KEY and not GOOGLE_API_KEY.startswith("your-"):
        return True
    return False

def use_mock() -> bool:
    """Determine whether to use mock simulation."""
    return MOCK_MODE or not is_api_configured()
