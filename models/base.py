from abc import ABC, abstractmethod
from typing import Optional


class BaseLLM(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a text response from a prompt."""
        pass

    @abstractmethod
    def generate_with_file(
        self,
        prompt: str,
        file_data: str,
        mime_type: str,
    ) -> str:
        """Generate a response from a prompt + file (e.g. base64 PDF)."""
        pass

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Return an embedding vector for the given text."""
        pass
