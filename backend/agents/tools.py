import webbrowser
import os
import platform
import subprocess
import datetime

from langchain_core.tools import tool


@tool
def open_application(app_name: str) -> str:
    try:
        if platform.system() == "Windows":
            subprocess.Popen(app_name)

        return f"{app_name} opened successfully"

    except Exception as e:
        return f"Error opening {app_name}: {e}"


@tool
def system_info(_: str = "") -> str:
    return f"""
        System: {platform.system()}
        Release: {platform.release()}
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        """


@tool
def calculator(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"Error: {e}"


@tool
def get_time(_: str = "") -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")


@tool
def get_date(_: str = "") -> str:
    return datetime.date.today().isoformat()


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

    if "time" in q:
        return get_time.invoke({})

    if "date" in q:
        return get_date.invoke({})

    if any(x in q for x in ["*", "+", "-", "/"]):
        return calculator.invoke({"expression": q})

    if "system" in q:
        return system_info.invoke({})

    return "Tool not recognized."


TOOLS = [
    open_application,
    system_info,
    calculator,
    get_time,
    get_date,
]
