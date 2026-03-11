from backend.llm.ollama_client import OllamaClient

llm = OllamaClient()

response = llm.generate(
    "Explain Retrieval-Augmented Generation (RAG) in one sentence", [], []
)

print(response)
