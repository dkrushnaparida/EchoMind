from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class OllamaClient:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2:3b", temperature=0.2)
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are EchoMind, an AI assistant.
            Use the following information to answer.

            Conversation History:
            {memory}

            Relevant Documents:
            {documents}

            User Question:
            {question}

            Provide a clear and accurate answer.
            """
        )

        self.chain = self.prompt | self.llm

    def generate(self, question: str, memory: str, documents: str):

        response = self.chain.invoke(
            {"question": question, "memory": memory, "documents": documents}
        )

        return response.content

    def stream(self, question: str, memory: str, documents: str):

        for chunk in self.chain.stream(
            {"question": question, "memory": memory, "documents": documents}
        ):
            if chunk.content:
                yield chunk.content
