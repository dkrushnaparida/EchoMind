from langchain_ollama import ChatOllama
from backend.core.config import config
from backend.core.logger import get_logger


logger = get_logger(__name__)


class OllamaClient:

    def __init__(self):
        self.model = config.ollama_model

        self.client = ChatOllama(model=self.model, temperature=0.2)

    def chat(self, message: str, history: list | None = None):
        if history is None:
            history = []

        messages = []

        # load history
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})

        # add current message
        messages.append({"role": "user", "content": message})

        try:
            response = self.client.invoke(messages)
            return response.content

        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return "Sorry, I encountered an error."
