import json
from pathlib import Path


class Config:
    def __init__(self):
        config_path = Path("configs/settings.json")
        with open(config_path, "r") as f:
            self.settings = json.load(f)

    @property
    def ollama_model(self):
        return self.settings.get("ollama_model", "llama3.2:3b")

    @property
    def embed_model(self):
        return self.settings.get("embed_model", "nomic-embed-text:latest")

    @property
    def postgres_url(self):
        return self.settings.get(
            "postgres_url",
            "postgresql://postgres:postgres@localhost:5432/echomind"
        )


config = Config()