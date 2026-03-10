from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class QueryRouter:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2:3b", temperature=0)
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a query classifier.
            Classify the user query into one of the categories:

            memory  -> question about previous conversation
            rag     -> question about uploaded documents
            tool    -> request to perform an action

            Respond ONLY with one word:
            memory, rag, or tool

            Query:
            {query}
            """
        )

        self.chain = self.prompt | self.llm

    def route(self, query: str):
        result = self.chain.invoke({"query": query})
        decision = result.content.strip().lower()

        return decision
