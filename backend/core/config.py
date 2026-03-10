import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

CONFIG_PATH = BASE_DIR / "configs" / "settings.json"


class Settings:

    def __init__(self):

        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)

        self.VECTOR_DB_DIR = config["vector_db_dir"]
        self.UPLOAD_DIR = config["upload_dir"]


settings = Settings()
