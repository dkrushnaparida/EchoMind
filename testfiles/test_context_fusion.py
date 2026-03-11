from backend.agents.context_fusion import build_context


class DummyDoc:
    def __init__(self, text):
        self.page_content = text


docs = [
    DummyDoc("Retrieval Augmented Generation combines retrieval with LLM."),
    DummyDoc("RAG improves factual accuracy."),
]

context = build_context(user_id="test_user", query="Explain RAG", documents=docs)

print(context)
