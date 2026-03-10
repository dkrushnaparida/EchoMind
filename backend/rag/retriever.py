from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.core.logger import get_logger

logger = get_logger(__name__)

VECTOR_DB_PATH = "data/vectordb"


def load_vector_db():
    embedding = OllamaEmbeddings(model="nomic-embed-text:latest")
    vectordb = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embedding)
    return vectordb


def create_retriever():
    vectordb = load_vector_db()
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    return retriever


def create_rag_chain():
    retriever = create_retriever()
    llm = ChatOllama(model="llama3.2:3b", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful AI assistant.
        Use the provided context to answer the question.
        Context:
        {context}
        Question:
        {question}
        Answer:
        """
    )

    chain = (
        {"context": retriever, "question": lambda x: x}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def ask_question(question: str):
    logger.info(f"User question: {question}")
    rag_chain = create_rag_chain()
    response = rag_chain.invoke(question)
    logger.info("Answer generated")

    return response


if __name__ == "__main__":

    while True:
        question = input("\nAsk something: ")
        if question.lower() in ["exit", "quit"]:
            break

        answer = ask_question(question)
        print("\nAnswer:\n", answer)
