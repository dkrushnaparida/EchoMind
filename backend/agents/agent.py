from backend.agents.router import QueryRouter
from backend.agents.context_fusion import build_context
from backend.llm.ollama_client import OllamaClient
from backend.agents.tools import run_tool

from backend.rag.retriever import RAGRetriever


router = QueryRouter()
llm = OllamaClient()
retriever = RAGRetriever()


def handle_query(user_id: str, query: str):
    route = router.route(query)
    print("ROUTER DECISION:", route)

    if route == "tool":
        return run_tool(query)

    docs = retriever.retrieve(query)

    context = build_context(query, user_id, docs)

    if route == "memory":
        return llm.generate(question=query, memory=context["memory"], documents="")

    elif route == "rag":
        return llm.generate(question=query, memory="", documents=context["documents"])

    else:
        return llm.generate(
            question=query, memory=context["memory"], documents=context["documents"]
        )
