from dotenv import load_dotenv 
import os

class Config():
    load_dotenv()

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "cvparser")
    DB_USER = os.getenv("DB_USER", "postgres")

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
