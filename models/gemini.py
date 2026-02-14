import logging
from google import genai
from google.genai import types
from models.base import BaseLLM

logger = logging.getLogger(__name__)


class GeminiLLM(BaseLLM):
    """Google Gemini LLM provider."""

    DEFAULT_MODEL = "models/gemini-2.5-flash"
    DEFAULT_EMBEDDING_MODEL = "text-embedding-004"

    def __init__(
        self,
        api_key: str,
        model_name: str = DEFAULT_MODEL,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    ):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.embedding_model = embedding_model
        logger.info("GeminiLLM initialised  model=%s", self.model_name)

    # ---- text generation ----

    def generate(self, prompt: str) -> str:
        logger.debug("generate() prompt length=%d", len(prompt))
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text

    # ---- multimodal generation (file + prompt) ----

    def generate_with_file(
        self,
        prompt: str,
        file_data: str,
        mime_type: str,
    ) -> str:
        """Send a base64-encoded file alongside a text prompt to Gemini."""
        logger.debug(
            "generate_with_file() mime=%s  data_len=%d",
            mime_type,
            len(file_data),
        )

        file_part = types.Part.from_bytes(
            data=__import__("base64").b64decode(file_data),
            mime_type=mime_type,
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[file_part, prompt],
        )
        return response.text

    # ---- embeddings ----

    def embed(self, text: str) -> list[float]:
        logger.debug("embed() text length=%d", len(text))
        response = self.client.models.embed_content(
            model=self.embedding_model,
            contents=text,
        )
        return response.embedding
