import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    # Database
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")

    # Redis
    REDIS_URL = os.getenv("REDIS_URL")

    # Ollama
    OLLAMA_URL = os.getenv("OLLAMA_URL")
    OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL")
    OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL")

    # LLM Params
    OLLAMA_LLM_PARAMS = {
        "temperature": float(os.getenv("OLLAMA_TEMPERATURE")),
        "top_k": int(os.getenv("OLLAMA_TOP_K")),
        "top_p": float(os.getenv("OLLAMA_TOP_P")),
        "repeat_penalty": float(os.getenv("OLLAMA_REPEAT_PENALTY")),
        "num_ctx": int(os.getenv("OLLAMA_NUM_CTX")),
    }

    @staticmethod
    def get_password():
        secret_file = os.getenv("DB_PASSWORD_FILE")
        if secret_file and os.path.exists(secret_file):
            with open(secret_file, "r") as f:
                return f.read().strip()

    @property
    def DATABASE_URL(self):
        password = self.get_password()
        return f"postgresql://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = Config()