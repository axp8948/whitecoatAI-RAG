import os
from models.gemini import GeminiLLM


def get_llm():
    return GeminiLLM(api_key=os.getenv("GEMINI_API_KEY"))

