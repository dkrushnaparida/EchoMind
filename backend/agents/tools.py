import webbrowser
import os


def run_tool(query: str):

    q = query.lower()

    if "open chrome" in q:
        webbrowser.open("https://www.google.com")
        return "Opening Chrome..."

    if "open youtube" in q:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube..."

    if "open folder" in q:
        os.startfile(os.getcwd())
        return "Opening project folder..."

    return "Tool not recognized."
