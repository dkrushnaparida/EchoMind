from backend.agents.tools import run_tool

queries = ["time", "date"]

for q in queries:
    result = run_tool(q)
    print(f"\nTool Query: {q}")
    print("Result:", result)
