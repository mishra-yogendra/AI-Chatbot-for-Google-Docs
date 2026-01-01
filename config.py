import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL = "llama-3.1-8b-instant"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 3
