from backend.llm.ollama_client import OllamaClient

llm = OllamaClient()


class ConversationSummarizer:
    def summarize(self, history):
        text = ""
        for msg in history:
            text += f"{msg['role']}: {msg['content']}\n"

        prompt = f"""
        Summarize this conversation shortly.
        {text}
        Summary:
        """

        return llm.chat(prompt)
