from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser


class OllamaClient:
    def __init__(
        self,
        model: str = "llama3.2:3b",
        temperature: float = 0.3,
    ):
        self.model = model
        self.temperature = temperature

        self.llm = ChatOllama(
            model=self.model,
            temperature=self.temperature,
        )

        self.parser = StrOutputParser()

    def generate(self, prompt: str) -> str:
        messages = [
            SystemMessage(content="You are EchoMind, a helpful AI assistant."),
            HumanMessage(content=prompt),
        ]

        response = self.llm.invoke(messages)
        return self.parser.invoke(response)

    def chat(self, prompt: str) -> str:
        return self.generate(prompt)


if __name__ == "__main__":

    llm = OllamaClient()

    question = "Explain what LangChain is in simple words."

    response = llm.chat(question)

    print("\nEchoMind Response:\n")
    print(response)
