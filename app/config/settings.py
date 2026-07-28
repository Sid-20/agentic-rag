
from dotenv import load_dotenv
import os


load_dotenv()

class Settings:

    OPENAI_KEY : str = os.getenv("OPENAI_KEY")
    OPENAI_MODEL : str = os.getenv("OPENAI_MODEL")