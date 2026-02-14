import chromadb
from chromadb.utils import embedding_functions
import os


class ChromaVectorStore:
    def __init__(self, persist_directory="chroma_db"):
        self.persist_directory = persist_directory

        self.client = chromadb.Client(
            settings=chromadb.config.Settings(
                persist_directory=self.persist_directory,
                is_persistent=True
            )
        )

        self.embedding_function = embedding_functions.GoogleGenerativeAIEmbeddingFunction(
            api_key=os.getenv("GEMINI_API_KEY"),
            model_name="models/embedding-001"
        )

        self.collection = self.client.get_or_create_collection(
            name="whitecoat_knowledge_base",
            embedding_function=self.embedding_function
        )

    def add_documents(self, chunks):
        """
        Add knowledge chunks to Chroma.
        Only call once for initial indexing.
        """
        documents = []
        metadatas = []
        ids = []

        for i, chunk in enumerate(chunks):
            documents.append(chunk["text"])
            metadatas.append({
                "topic": chunk["topic"],
                "filename": chunk["filename"],
                "source": chunk["source"]
            })
            ids.append(f"{chunk['filename']}_{i}")

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query, top_k=5):
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        return results
