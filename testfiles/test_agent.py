from backend.agents.agent import handle_query

queries = [
    "What is Retrieval Augmented Generation?",
    "What did I ask earlier?",
]

user_id = "test_user"

for q in queries:
    print("\n============================")
    print("User:", q)

    response = handle_query(user_id, q)

    print("Assistant:", response)
