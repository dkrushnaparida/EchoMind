import webbrowser
import os
import platform
import subprocess

from langchain_core.tools import tool
import datetime


@tool
def open_application(app_name: str) -> str:
    """
    Open a given application by name.

    Args:
        app_name (str): The name of the application to open.
                       On Windows, this is passed directly to subprocess.Popen.

    Returns:
        str: A success message if the application opens,
             or an error message if the operation fails.
    """
    try:
        if platform.system() == "Windows":
            subprocess.Popen(app_name)

        return f"{app_name} opened successfully"

    except Exception as e:
        return f"Error opening {app_name}: {e}"


@tool
def system_info(_: str = "") -> str:
    """
    Retrieve basic system information.

    Args:
        _ (str, optional): Placeholder argument (not used).
                           Defaults to an empty string.

    Returns:
        str: A formatted string containing system details such as
             operating system, release version, machine type, and processor.
    """
    return f"""
        System: {platform.system()}
        Release: {platform.release()}
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        """


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.

    Args:
        expression (str): A string containing a valid Python expression
                          (e.g., "2+2", "3*5", "10/2").

    Returns:
        str: The result of the evaluated expression as a string,
             or an error message if evaluation fails.
    """
    try:
        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"Error: {e}"


@tool
def get_time():
    """Return the current system time."""
    return datetime.datetime.now().strftime("%H:%M:%S")


@tool
def get_date():
    """Return today's date."""
    return datetime.date.today().isoformat()


def run_tool(query: str):
    """
    Execute a predefined tool action based on a query string.

    Args:
        query (str): A user query describing the desired action.
                     Supported queries include:
                     - "open chrome": Opens Google Chrome in a browser.
                     - "open youtube": Opens YouTube in a browser.
                     - "open folder": Opens the current working directory.

    Returns:
        str: A message describing the action taken,
             or "Tool not recognized." if the query does not match.
    """
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

    elif "date" in q:
        return get_date.invoke({})

    return "Tool not recognized."


TOOLS = [
    open_application,
    system_info,
    calculator,
]
