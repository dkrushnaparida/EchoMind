from backend.agents.agent import handle_query

queries = [
    "What is Retrieval Augmented Generation?",
    "My favorite framework is RAG",
    "Explain my favorite framework",
    "what time is it",
]

user_id = "test_user"

for q in queries:
    print("\n============================")
    print("User:", q)

    response = handle_query(user_id, q)

    print("Assistant:", response)
