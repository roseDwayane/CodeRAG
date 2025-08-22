import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# === Environment Variables ===
# Model provider settings (loaded from .env)
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")  # "openai" or "ollama"

# OpenAI API key and model settings (loaded from .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")  # Default to ada-002
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4")  # Default to GPT-4

# Ollama settings (loaded from .env)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")  # Default Ollama URL
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama2")  # Default Ollama model
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "llama2")  # Default Ollama embedding model

# Embedding dimension (from .env or fallback)
# Note: Different models have different embedding dimensions
# OpenAI text-embedding-ada-002: 1536
# Ollama llama2: 4096 (may vary by model)
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", 1536))  # Default to 1536 if not in .env

# Project directory (from .env)
WATCHED_DIR = os.getenv("WATCHED_DIR", os.path.join(os.getcwd(), 'CodeRAG'))

# Path to FAISS index (from .env or fallback)
FAISS_INDEX_FILE = os.getenv("FAISS_INDEX_FILE", os.path.join(WATCHED_DIR, 'coderag_index.faiss'))

# === Project-Specific Configuration ===
# Define the root directory of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Additional directories to ignore during indexing (these can remain static)
IGNORE_PATHS = [
    os.path.join(WATCHED_DIR, ".venv"),
    os.path.join(WATCHED_DIR, "node_modules"),
    os.path.join(WATCHED_DIR, "__pycache__"),
    os.path.join(WATCHED_DIR, ".git"),
    os.path.join(WATCHED_DIR, "tests"),
]
