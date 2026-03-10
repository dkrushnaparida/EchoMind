from backend.agents.router import QueryRouter
from backend.agents.context_fusion import build_context
from backend.llm.ollama_client import OllamaClient
from backend.agents.tools import run_tool


router = QueryRouter()
llm = OllamaClient()


def handle_query(user_id: str, query: str):
    route = router.route(query)
    print("ROUTER DECISION:", route)
    if route == "memory":
        context = build_context(query, user_id)
        return llm.generate(question=query, memory=context["memory"], documents="")

    elif route == "rag":
        context = build_context(query, user_id)
        return llm.generate(question=query, memory="", documents=context["documents"])

    elif route == "tool":
        return run_tool(query)

    else:
        context = build_context(query, user_id)

        return llm.generate(
            question=query, memory=context["memory"], documents=context["documents"]
        )
