import os
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    if os.getenv("RAILWAY_ENVIRONMENT") is None:
        load_dotenv()  # Only load .env in local/dev environments
    
    
    if not os.getenv("GROQ_API_KEY"):
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Add it to your .env file or environment."
        )