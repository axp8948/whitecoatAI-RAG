import logging
import openai
from models.base import BaseLLM

logger = logging.getLogger(__name__)


class OpenAILLM(BaseLLM):
    """OpenAI LLM provider."""

    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

    def __init__(
        self,
        api_key: str,
        model_name: str = DEFAULT_MODEL,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    ):
        self.openai_client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name
        self.embedding_model = embedding_model
        logger.info("OpenAILLM initialised  model=%s", self.model_name)

    # ---- text generation ----

    def generate(self, prompt: str) -> str:
        logger.debug("generate() prompt length=%d", len(prompt))
        response = self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    # ---- multimodal generation (file + prompt) ----

    def generate_with_file(
        self,
        prompt: str,
        file_data: str,
        mime_type: str,
    ) -> str:
        """Send a base64-encoded file alongside a text prompt to OpenAI vision."""
        logger.debug(
            "generate_with_file() mime=%s  data_len=%d",
            mime_type,
            len(file_data),
        )

        image_url = f"data:{mime_type};base64,{file_data}"

        response = self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content

    # ---- embeddings ----

    def embed(self, text: str) -> list[float]:
        logger.debug("embed() text length=%d", len(text))
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text,
        )
        return response.data[0].embedding
