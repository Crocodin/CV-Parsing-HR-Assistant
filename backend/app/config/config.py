from dotenv import load_dotenv 
import os

class Config():
    load_dotenv()

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "cvparser")
    DB_USER = os.getenv("DB_USER", "postgres")

    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "cv-parser")
    OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

    OLLAMA_LLM_PARAMS = {
        "temperature": 0.7,
        "seed": 0,
        "top_k": 5,
        "top_p": 0.2,
        "min_p": 0.0,
        "repeat_penalty": 1.05
    }

    @staticmethod
    def get_password():
        secret_file = os.getenv("DB_PASSWORD_FILE")
        if secret_file and os.path.exists(secret_file):
            with open(secret_file) as f:
                return f.read().strip()
        return os.getenv("DB_PASSWORD", "password")

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.get_password()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

config = Config()
