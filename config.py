import os

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


class Config:

    # Flask secret key
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "default-secret-key"
    )

    # Database
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///career_ai.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Groq API key
    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY",
        ""
    )