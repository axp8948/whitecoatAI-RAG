from rag.loader import KnowledgeBaseLoader
from rag.chroma_store import ChromaVectorStore


class RAGEngine:
    def __init__(self, kb_path="knowledge_base"):
        self.loader = KnowledgeBaseLoader(kb_path)
        self.store = ChromaVectorStore()

        if self.store.collection.count() == 0:
            print("Indexing knowledge base...")
            chunks = self.loader.load()

            documents = []
            ids = []
            metadatas = []

            for i, chunk in enumerate(chunks):
                documents.append(chunk["text"])
                ids.append(f"{chunk['filename']}_{i}")
                metadatas.append({
                    "topic": chunk["topic"],
                    "filename": chunk["filename"],
                    "source": chunk["source"]
                })

            self.store.add_documents(documents, ids, metadatas)
            print("Indexing complete.")
        else:
            print("Knowledge base already indexed.")

    def retrieve(self, query, top_k=5):
        return self.store.query(query, n_results=top_k)
