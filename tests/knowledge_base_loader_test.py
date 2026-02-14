from rag.loader import KnowledgeBaseLoader


loader = KnowledgeBaseLoader("knowledge_base")
chunks = loader.load()

print("Total chunks:", len(chunks))
print(chunks[0]["text"])


lengths = [len(c["text"]) for c in chunks]
print("Max length:", max(lengths))
print("Min length:", min(lengths))
print("Average length:", sum(lengths)//len(lengths))
