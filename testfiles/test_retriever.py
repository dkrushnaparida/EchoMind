from backend.rag.retriever import RAGRetriever

retriever = RAGRetriever()

docs = retriever.retrieve("What is Retrieval Augmented Generation?")

print("Number of docs:", len(docs))
print("\nTop result:\n")
print(docs[0].page_content)
