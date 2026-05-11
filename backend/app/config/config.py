from dotenv import load_dotenv 
import os

class Config():
    load_dotenv()  # Load environment variables from .env file

    DATABASE_URL: str = os.getenv("DATABASE_URL")

config = Config()
