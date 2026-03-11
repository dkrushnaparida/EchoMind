def calculator_tool(query: str):

    try:
        result = eval(query)
        return f"Result: {result}"

    except Exception:
        return "Invalid calculation"
