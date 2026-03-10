from langchain_ollama import ChatOllama
from backend.core.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:

    def __init__(self, model: str = "llama3.2:3b", temperature: float = 0.3):

        logger.info(f"Initializing Ollama model: {model}")

        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
        )

    def get_llm(self):
        return self.llm
