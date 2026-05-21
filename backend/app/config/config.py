import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    # Database
    DB_HOST = os.getenv("POSTGRES_HOST", "db")
    DB_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    DB_NAME = os.getenv("POSTGRES_DB", "cvparser")
    DB_USER = os.getenv("POSTGRES_USER", "postgres")

    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

    # Ollama
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "granite4.1:3b")
    OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "embeddinggemma:300m")

    # LLM Params
    OLLAMA_LLM_PARAMS = {
        "temperature": float(os.getenv("OLLAMA_TEMPERATURE", 0.4)),
        "top_k": int(os.getenv("OLLAMA_TOP_K", 10)),
        "top_p": float(os.getenv("OLLAMA_TOP_P", 0.8)),
        "repeat_penalty": float(os.getenv("OLLAMA_REPEAT_PENALTY", 1.05)),
        "num_ctx": int(os.getenv("OLLAMA_NUM_CTX", 6144)),
    }

    @staticmethod
    def get_password():
        secret_file = os.getenv("POSTGRES_PASSWORD_FILE")

        if secret_file and os.path.exists(secret_file):
            with open(secret_file, "r") as f:
                return f.read().strip()

        return os.getenv("POSTGRES_PASSWORD")

    @property
    def DATABASE_URL(self):
        password = self.get_password()
        return f"postgresql://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = Config()