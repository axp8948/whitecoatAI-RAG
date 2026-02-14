from rag.orchestrator import RAGEngine

rag = RAGEngine("knowledge_base")

results = rag.retrieve("What does low hemoglobin mean?", top_k=5)

docs = results["documents"][0]
metas = results["metadatas"][0]

for doc, meta in zip(docs, metas):
    print("Topic:", meta["topic"])
    print("Preview:", doc[:200])
    print("-" * 50)
