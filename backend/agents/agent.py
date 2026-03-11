from backend.agents.router import QueryRouter
from backend.agents.context_fusion import build_context
from backend.llm.ollama_client import OllamaClient
from backend.agents.tools import run_tool
from backend.memory.postgres_memory import save_message
from backend.rag.retriever import RAGRetriever


router = QueryRouter()
llm = OllamaClient()
retriever = RAGRetriever()


def handle_query(user_id: str, query: str):
    save_message(user_id, "user", query)

    route = router.route(query)

    # print("ROUTER DECISION:", route)

    if route == "tool":
        response = run_tool(query)

    else:
        docs = retriever.retrieve(query)

        context = build_context(user_id, query, docs)

        if route == "memory":
            response = llm.generate(
                question=query, memory=context["memory"], documents=""
            )

        elif route == "rag":
            response = llm.generate(
                question=query, memory="", documents=context["documents"]
            )

        else:
            response = llm.generate(
                question=query, memory=context["memory"], documents=context["documents"]
            )
    save_message(user_id, "assistant", response)

    return response
