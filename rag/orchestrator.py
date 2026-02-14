from rag.loader import KnowledgeBaseLoader
from rag.chroma_store import ChromaVectorStore


class RAGEngine:
    def __init__(self, kb_path="knowledge_base"):
        self.loader = KnowledgeBaseLoader(kb_path)
        self.store = ChromaVectorStore()

        # Check if collection already populated
        if self.store.collection.count() == 0:
            print("Indexing knowledge base...")
            chunks = self.loader.load()
            self.store.add_documents(chunks)
            print("Indexing complete.")
        else:
            print("Knowledge base already indexed.")

    def retrieve(self, query, top_k=5):
        results = self.store.search(query, top_k=top_k)
        return results
