from backend.agents.router import QueryRouter

router = QueryRouter()

queries = [
    "What is Retrieval Augmented Generation?",
    "What did I say earlier?",
    "open calculator",
]

for q in queries:
    route = router.route(q)
    print(f"\nQuery: {q}")
    print("Route:", route)
