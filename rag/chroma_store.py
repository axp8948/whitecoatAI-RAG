import os
import chromadb
from google import genai
from google.genai import types
from chromadb import EmbeddingFunction
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv() 

class OpenAIEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name: str = "text-embedding-3-small"):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found.")

        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.batch_size = 100

    def __call__(self, input):
        all_embeddings = []

        for i in range(0, len(input), self.batch_size):
            batch = input[i:i + self.batch_size]

            response = self.client.embeddings.create(
                model=self.model_name,
                input=batch
            )

            batch_embeddings = [e.embedding for e in response.data]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings



# Gemini embedding model has a hard rate limit - free tier
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __init__(self, api_key: str = None, model_name: str = "models/gemini-embedding-001"):
        from dotenv import load_dotenv
        load_dotenv()

        api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.batch_size = 100  # Gemini limit

    def __call__(self, input):
        all_embeddings = []

        # Process in batches of 100
        for i in range(0, len(input), self.batch_size):
            batch = input[i:i + self.batch_size]

            result = self.client.models.embed_content(
                model=self.model_name,
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT"
                )
            )

            batch_embeddings = [e.values for e in result.embeddings]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings



class ChromaVectorStore:
    def __init__(self, persist_directory="chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)

        self.embedding_function = OpenAIEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name="whitecoat_knowledge_base",
            embedding_function=self.embedding_function
        )

    def add_documents(self, documents, ids, metadatas=None):
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def query(self, query_text, n_results=5):
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
