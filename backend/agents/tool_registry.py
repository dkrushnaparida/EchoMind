from backend.tools.calculator import calculator_tool
from backend.tools.weather import weather_tool


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, func):
        self.tools[name] = func

    def get(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())


registry = ToolRegistry()

registry.register("calculator", calculator_tool)
registry.register("weather", weather_tool)
