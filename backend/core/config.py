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

        self.DB_HOST = config["db_host"]
        self.DB_PORT = config["db_port"]
        self.DB_NAME = config["db_name"]
        self.DB_USER = config["db_user"]
        self.DB_PASSWORD = config["db_password"]


settings = Settings()
