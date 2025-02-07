import os
from dotenv import load_dotenv

# Derive ENV_PATH from K_PATH if provided
K_PATH = os.getenv("K_PATH")
if K_PATH:
    ENV_PATH = os.path.join(K_PATH, ".env")
else:
    raise ValueError("K_PATH environment variable must be set")


class Config:
    """
    A configuration service that reads environment variables
    and falls back to values defined in a .env file.
    """

    def __init__(self, dotenv_path: str = ENV_PATH):
        """
        Initialize the Config service, loading the .env file.
        
        :param dotenv_path: The path to the .env file (default is ".env" or as specified by ENV_PATH).
        """
        # Load environment variables from dotenv_path, but do NOT override
        # already-set environment variables
        load_dotenv(dotenv_path, override=False)

    def get(self, key: str, default=None):
        """
        Return the value for environment variable `key`.
        If it's not found, return `default`.
        """
        return os.getenv(key, default)

    def require(self, key: str):
        """
        Return the value for environment variable `key`.
        Raises an error if not found.
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' is not set.")
        return value
