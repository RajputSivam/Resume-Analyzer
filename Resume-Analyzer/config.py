from dotenv import load_dotenv
import os

load_dotenv()


class Config:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MODEL = os.getenv("MODEL", "llama-3.1-8b-instant")

    TEMPERATURE = float(os.getenv("TEMPERATURE", 0))