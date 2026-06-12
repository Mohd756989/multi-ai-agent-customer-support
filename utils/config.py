import os
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Add it to your .env file or environment."
        )
